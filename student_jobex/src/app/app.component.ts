import {Component, ViewChild} from '@angular/core';
import {LoadingController, MenuController, NavController, Platform} from 'ionic-angular';
import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';
import { HomePage } from '../pages/home/home';
import {LoginPage} from "../pages/login/login";
import {RegisterPage} from "../pages/register/register";
import {MyProfilePage} from "../pages/my-profile/my-profile";


@Component({
  templateUrl: 'app.html'
})
export class MyApp {
  homePage = HomePage;
  loginPage = LoginPage;
  registerPage = RegisterPage;
  myProfilePage = MyProfilePage;
  isAuthenticated:boolean;

  @ViewChild('nav') nav: NavController;

  constructor(platform: Platform, statusBar: StatusBar, splashScreen: SplashScreen,
              private menuCtrl: MenuController , private loaderCtrl: LoadingController) {

    platform.ready().then(() => {
      // Okay, so the platform is ready and our plugins are available.
      // Here you can do any higher level native things you might need.
      this.onAuthenticationCheck();
      statusBar.styleDefault();
      splashScreen.hide();
    });

  }

  onLoad(page:any){
    this.nav.setRoot(page);
    this.menuCtrl.close();
  }

  onAuthenticationCheck(){
    const loader = this.loaderCtrl.create({
      content:'Loading...'
    });
    loader.present();
    let t = setTimeout(() => {
      /*if (localStorage.getItem('access_token') != null && localStorage.getItem('refresh_token') != null) {
        console.log('authenticated');
        this.isAuthenticated = true;
        this.nav.setRoot(this.homePage);
      }
      else {
        console.log('not authenticated');
        //this.nav.setRoot(this.loginPage);
        this.isAuthenticated = false;
      }
      */
      this.isAuthenticated = true;
      this.nav.setRoot(this.myProfilePage);
      loader.dismiss();
    },100);

  }

}

