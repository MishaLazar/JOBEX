import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';
import { SplashScreen } from '@ionic-native/splash-screen';
import { StatusBar } from '@ionic-native/status-bar';

import { MyApp } from './app.component';
import { HomePage } from '../pages/home/home';
import {LoginPage} from "../pages/login/login";
import {RegisterPage} from "../pages/register/register";
import {AuthenticationService} from "../services/authentication.service";
import {HttpClientModule} from "@angular/common/http";
import {ConfigService} from "../services/config.service";
import {IonicStorageModule } from "@ionic/storage";
import {StorageService} from "../services/storage.service";
/*import { JwtModule } from '@auth0/angular-jwt';*/

@NgModule({
  declarations: [
    MyApp,
    HomePage,
    LoginPage,
    RegisterPage
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    IonicModule.forRoot(MyApp),
    IonicStorageModule.forRoot(),
    /*JwtModule.forRoot({
      config:{
        tokenGetter: function tokenGetter() {
          return  localStorage.getItem('access_token');
        },
        blacklistedRoutes : ['http://127.0.0.1:5050/login']
      }
    })*/
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    HomePage,
    LoginPage,
    RegisterPage
  ],
  providers: [
    StatusBar,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},AuthenticationService,ConfigService,StorageService
  ]
})
export class AppModule {}
