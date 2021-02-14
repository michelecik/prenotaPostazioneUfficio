from flask import Flask, jsonify, session, request, redirect, abort, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_cors import CORS, cross_origin
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import json
import os
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:CiaoCiao88@localhost:3306/appprenotascrivanie'

app.config['SECRET_KEY'] = 'SECRET'
app.secret_key =  'superSecretKey'

SESSION_USERID = None

db = SQLAlchemy(app)

api = Api(app)

CORS(app)

USERLOGGED = False

# - fase di login (utente + password + reset password via mail)
# - TODO: resetPassword()


# DB MODELS
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String)
    password = db.Column(db.String)
    id_ruolo = db.Column(db.Integer)
    attivo = db.Column(db.Boolean)

class Prenotazione(db.Model):
    __tablename__ = 'prenotazione'
    id = db.Column(db.Integer, primary_key=True)
    numero_prenotazione = db.Column(db.Integer)
    id_utente = db.Column(db.Integer)
    data = db.Column(db.Date)
    ora_inizio = db.Column(db.Time)
    ora_fine = db.Column(db.Time)
    id_postazione = db.Column(db.Integer)

class Postazione(db.Model):
    __tablename__ = 'postazione'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    id_piano = db.Column(db.Integer)

class Ruolo(db.Model):
    __tablename__ = 'ruolo'
    id = db.Column(db.Integer, primary_key=True)
    ruolo = db.Column(db.String)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # controlla se è presente x-access-token
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']


        if not token:
            return jsonify({'message':'token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'}), 401

        return f(current_user, *args, **kwargs)
    
    return decorated

# ROUTES
@app.route('/user', methods=['POST'])
@token_required
def signIn(current_user):
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    newUser = User(public_id=str(uuid.uuid4()), username=data['username'], email=data['email'], password=hashed_password, id_ruolo=data['ruolo'], attivo=1)
    db.session.add(newUser)
    db.session.commit()

    return jsonify({'message': 'new user created'})

@app.route('/users', methods=['GET'])
@token_required
def getAllUsers(current_user):
    allUsers = User.query.all()

    output = []

    for user in allUsers:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['ruolo'] = user.id_ruolo
        output.append(user_data)
    
    return jsonify({'users': output})

# @app.route('/user-reservations', methods=['GET'])
# @token_required
# def getUserReservations(current_user):
#     userReservations = Prenotazione.query.filter(Prenotazione.id_utente == current_user.id).all()
        
#     output = []

#     for reservation in userReservations:
#         reservation_data = {}
#         reservation_data['id'] = reservation.id
#         reservation_data['numero_prenotazione'] = reservation.numero_prenotazione
#         reservation_data['data'] = str(reservation.data)
#         reservation_data['ora_inizio'] = str(reservation.ora_inizio)
#         reservation_data['ora_fine'] = str(reservation.ora_fine)
#         reservation_data['id_postazione'] = reservation.id_postazione
#         output.append(reservation_data)
    
#     return jsonify({'reservations': output})

@app.route('/user-reservations', methods=['GET'])
@token_required
def getUserReservations(current_user):
    userReservationsNumber = db.engine.execute('SELECT distinct numero_prenotazione FROM prenotazione WHERE id_utente = %s', current_user.id)
        
    output = []

    for reservationNumber in userReservationsNumber:
        res_data = {}
        res_data['numero_prenotazione'] = str(reservationNumber[0])
        res_data['postazioni'] = []
        queryPostazioni = db.engine.execute('SELECT * FROM prenotazione WHERE numero_prenotazione = %s', reservationNumber)
        for postazione in queryPostazioni:
            res_data['id'] = postazione.id
            res_data['postazioni'].append(str(postazione.id_postazione))
            res_data['ora_inizio'] = str(postazione.ora_inizio)
            res_data['ora_fine'] = str(postazione.ora_fine)
            res_data['data'] = str(postazione.data)
        output.append(res_data)

    for resNumb in userReservationsNumber:
        print(resNumb)
    
    return jsonify({'reservations': output})

@app.route('/postazioni', methods=['POST'])
@token_required
def getPostazioniOccupate(current_user):
    data = request.get_json()

    # PRENDO TUTTE LE PRENOTAZIONI/POSTAZIONI OCCUPATE PER QUEL GIORNO IN QUELLA FASCIA ORARIA... teoricamente

    # SELEZIONA SE LA PRENOTAZIONE INIZIA PRIMA DI DATA[ora_fine]
    # SELEZIONA SE LA PRENOTAZIONE FINISCE DOPO DI DATA['ora_inizio]

    # BUGGO : LA QUERY SELEZIONA ANCHE LE PRENOTAZIONI CHE FINISCONO ESATTAMENTE ALL'ORA A CUI LA NUOVA PRENOTAZIONE INIZIA
    
    prenotazioniDelGiorno = Prenotazione.query.filter(
        Prenotazione.data == data['dataPrenotazione'],
        or_(Prenotazione.ora_inizio.between(data['oraInizio'], data['oraFine']),Prenotazione.ora_fine.between(data['oraInizio'], data['oraFine'])))

    output = []

    for prenotazione in prenotazioniDelGiorno:
        prenotazione_data = {}
        prenotazione_data['id_utente'] = prenotazione.id_utente 
        prenotazione_data['id_postazione'] = prenotazione.id_postazione
        prenotazione_data['data'] = str(prenotazione.data)
        prenotazione_data['ora_inizio'] = str(prenotazione.ora_inizio)
        output.append(prenotazione_data)

    return jsonify({'postazioni':output})


@app.route('/prenotazione', methods=['POST'])
@token_required
def addPrenotazione(current_user):
    data = request.get_json()
    print(data)


    if data['dataPrenotazione'] == '' or data['oraInizio'] == '' or data['oraFine'] == '':
        return jsonify({'error': 'Devi selezionare una data e un orario validi per prenotare'})
    
    # generare un numero_prenotazione da assegnare alla prenotazione che essa sia singola o multipla
    numero_prenotazione = str(random.randint(1,21)*random.randint(1,21))

    # se è utente base
    if(current_user.id_ruolo == 3):
        newPrenotazione = Prenotazione(id_utente = current_user.id, numero_prenotazione=numero_prenotazione, data = data['dataPrenotazione'], ora_inizio = data['oraInizio'], ora_fine = data['oraFine'], id_postazione = data['postazione'])
        db.session.add(newPrenotazione)
        db.session.commit()
        return jsonify({'success': 'Prenotazione effettuata'})
    else:
        for postazione in data['postazione']:
            newPrenotazione = Prenotazione(id_utente = current_user.id, numero_prenotazione=numero_prenotazione, data = data['dataPrenotazione'], ora_inizio = data['oraInizio'], ora_fine = data['oraFine'], id_postazione = postazione)
            db.session.add(newPrenotazione)
        
        db.session.commit()
        return jsonify({'success': 'Prenotazione multipla effettuata'})


@app.route('/prenotazione/<id_prenotazione>', methods=['GET'])
@token_required
def getOnePrenotazione(current_user, id_prenotazione):
    prenotazione = Prenotazione.query.filter(Prenotazione.id == id_prenotazione)

    if not prenotazione:
        return jsonify({'message': 'No prenotazione found'})
    
    print(prenotazione)
    
    return jsonify({'results': prenotazione})

@app.route('/prenotazione/<num_prenotazione>', methods=['DELETE'])
@token_required
def deletePrenotazione(current_user, num_prenotazione):
    toDelete = Prenotazione.query.filter(Prenotazione.numero_prenotazione == num_prenotazione).all()

    if not toDelete:
        return jsonify({'message' : 'No prenotazione found!'})

    for pren in toDelete:
        db.session.delete(pren)

    db.session.commit()

    return jsonify({'message': 'Prenotazione has been deleted'})

@app.route('/login')
def login():
    auth = request.authorization
    print(auth)
    if not auth or not auth.username or not auth.password:
        return make_response('NOT AUTH OR AUTH.USERNAME', 401, {'WWW-Authenticate' : 'Basic realm="login required"'})
    
    user = User.query.filter(User.username == auth.username, User.attivo == 1).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="login required"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, app.config['SECRET_KEY'])

        user_data = {}

        user_data['username'] = user.username
        user_data['ruolo'] = user.id_ruolo


        return jsonify({'token': token.decode('UTF-8'), 'user': user_data})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="login required"'})

if __name__ == '__main__':
    app.run(port=5000)