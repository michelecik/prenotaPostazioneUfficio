-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Giu 11, 2019 alle 17:38
-- Versione del server: 10.1.38-MariaDB
-- Versione PHP: 7.3.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `appprenotascrivanie`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `prenotazione`
--

CREATE TABLE `prenotazione` (
  `id` int(11) NOT NULL,
  `numero_prenotazione` int(11) NOT NULL,
  `id_utente` int(11) NOT NULL,
  `data` date NOT NULL,
  `ora_inizio` time NOT NULL,
  `ora_fine` time NOT NULL,
  `id_postazione` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `prenotazione`
--

INSERT INTO `prenotazione` (`id`, `numero_prenotazione`, `id_utente`, `data`, `ora_inizio`, `ora_fine`, `id_postazione`) VALUES
(115, 31222, 4, '2019-06-13', '12:00:00', '16:00:00', 217),
(116, 31222, 4, '2019-06-13', '12:00:00', '16:00:00', 218),
(117, 31222, 4, '2019-06-13', '12:00:00', '16:00:00', 219),
(118, 31222, 4, '2019-06-13', '12:00:00', '16:00:00', 220),
(129, 1101003, 4, '2019-06-21', '12:00:00', '18:00:00', 204),
(130, 1101003, 4, '2019-06-21', '12:00:00', '18:00:00', 205),
(131, 1101003, 4, '2019-06-21', '12:00:00', '18:00:00', 206),
(132, 12685, 4, '2019-06-11', '08:00:00', '13:00:00', 210),
(133, 12685, 4, '2019-06-11', '08:00:00', '13:00:00', 211),
(134, 12685, 4, '2019-06-11', '08:00:00', '13:00:00', 212),
(135, 12685, 4, '2019-06-11', '08:00:00', '13:00:00', 213),
(136, 12, 4, '2019-06-12', '08:00:00', '13:00:00', 217),
(137, 12, 4, '2019-06-12', '08:00:00', '13:00:00', 218),
(138, 12, 4, '2019-06-12', '08:00:00', '13:00:00', 219),
(139, 12, 4, '2019-06-12', '08:00:00', '13:00:00', 220);

-- --------------------------------------------------------

--
-- Struttura della tabella `ruolo`
--

CREATE TABLE `ruolo` (
  `id` int(11) NOT NULL,
  `ruolo` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `ruolo`
--

INSERT INTO `ruolo` (`id`, `ruolo`) VALUES
(1, 'admin'),
(2, 'manager'),
(3, 'user');

-- --------------------------------------------------------

--
-- Struttura della tabella `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `public_id` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL DEFAULT '',
  `id_ruolo` int(11) NOT NULL DEFAULT '3',
  `attivo` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `user`
--

INSERT INTO `user` (`id`, `public_id`, `username`, `email`, `password`, `id_ruolo`, `attivo`) VALUES
(2, '0d4c6e44-41b4-4ca2-958a-c37d655851ec', 'testAdmin', 'email@gmail.com', 'sha256$CaFJdR6B$cc997ef2673e01a7408a4e89827c41ad78caa5068792443bef6c83efaf2e9990', 1, 1),
(4, 'b53a69d6-04a7-416f-8418-eaf8d0acc2d1', 'testManager', 'manager@gmail.com', 'sha256$5BePwzcj$ab837e4fb265e143e7c623a06753a6b6b410822834b29f9c7183bd28dd82f6b9', 2, 1),
(5, '49ecbd73-2afb-42e2-b94e-6d35fd9f8bac', 'testUser', 'user@gmail.com', 'sha256$LphtFkPZ$9aa077bc7f4fa243859a10f3c4cf7b33a02fdc4e6826c081518d4cdc2284206f', 3, 1);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `prenotazione`
--
ALTER TABLE `prenotazione`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `ruolo`
--
ALTER TABLE `ruolo`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `public_id` (`public_id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `prenotazione`
--
ALTER TABLE `prenotazione`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=140;

--
-- AUTO_INCREMENT per la tabella `ruolo`
--
ALTER TABLE `ruolo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT per la tabella `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
