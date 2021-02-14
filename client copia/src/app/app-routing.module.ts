import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { BiggerComponent } from './bigger/bigger.component';
import { AuthGuard } from './auth.guard';
import { UserReservationsComponent } from './user-reservations/user-reservations.component';
import { NewUserFormComponent } from './new-user-form/new-user-form.component';
import { UsersListComponent } from './users-list/users-list.component';

const routes: Routes = [
  {path: '', redirectTo: 'app', pathMatch: 'full'},
  {path: 'login', component: LoginComponent},
  {path: 'app', canActivate: [AuthGuard], component: BiggerComponent},
  {path: 'reservations', canActivate: [AuthGuard], component: UserReservationsComponent},
  {path: 'newuser', canActivate: [AuthGuard], component: NewUserFormComponent },
  {path: 'users', canActivate: [AuthGuard], component: UsersListComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
