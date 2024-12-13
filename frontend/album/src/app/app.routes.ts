import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';  
import { HomeComponent } from './components/home/home.component';  
import { NavegationComponent } from './components/navegation/navegation.component';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'home', component: HomeComponent },  
  { path: 'navegation', component: NavegationComponent },  
  { path: '**', redirectTo: '/login' },
];

