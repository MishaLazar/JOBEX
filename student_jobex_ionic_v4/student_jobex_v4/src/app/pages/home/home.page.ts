import { Component } from '@angular/core';
import {LoginPage} from "../login/login.page";
import {RegisterPage} from "../register/register.page";
import {MyProfilePage} from "../my-profile/my-profile.page";

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
    homePage = HomePage;
    loginPage = LoginPage;
    registerPage = RegisterPage;
    myProfilePage = MyProfilePage;
    isAuthenticated: boolean = false;


}
