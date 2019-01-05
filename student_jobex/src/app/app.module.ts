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
    IonicModule.forRoot(MyApp)
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
    {provide: ErrorHandler, useClass: IonicErrorHandler},AuthenticationService,ConfigService
  ]
})
export class AppModule {}
