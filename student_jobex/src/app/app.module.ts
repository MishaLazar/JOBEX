import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import {IonicApp, IonicErrorHandler, IonicModule} from 'ionic-angular';
import { SplashScreen } from '@ionic-native/splash-screen';
import { StatusBar } from '@ionic-native/status-bar';

import { MyApp } from './app.component';
import { HomePage } from '../pages/home/home';
import {LoginPage} from "../pages/login/login";
import {RegisterPage} from "../pages/register/register";
import {MyProfilePage} from "../pages/my-profile/my-profile";
import {AuthenticationService} from "../services/authentication.service";
import {HttpClientModule} from "@angular/common/http";
import {ConfigService} from "../services/config.service";

import {IonicStorageModule } from "@ionic/storage";
import {StorageService} from "../services/storage.service";
import {MyProfileService} from "../services/my-profile.service";

import {ComponentsModule } from "../components/components.module";
import {PersonalDataPage} from "../pages/personal-data/personal-data";
import {PersonalDataPageModule} from "../pages/personal-data/personal-data.module";



@NgModule({
  declarations: [
    MyApp,
    HomePage,
    LoginPage,
    RegisterPage,
    MyProfilePage
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ComponentsModule,
    PersonalDataPageModule,
    IonicModule.forRoot(MyApp),
    IonicStorageModule.forRoot()
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    HomePage,
    LoginPage,
    RegisterPage,
    MyProfilePage
  ],
  providers: [
    StatusBar,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
    AuthenticationService,
    ConfigService,
    StorageService,
    MyProfileService
  ]
})
export class AppModule {}
