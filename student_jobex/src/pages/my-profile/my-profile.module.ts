import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { MyProfilePage } from './my-profile';
import {PersonalDataPage} from "../personal-data/personal-data";


@NgModule({
  declarations: [MyProfilePage,PersonalDataPage],
  imports: [

    IonicPageModule.forChild(MyProfilePage),
  ],entryComponents:[PersonalDataPage]


})
export class MyProfilePageModule {}
