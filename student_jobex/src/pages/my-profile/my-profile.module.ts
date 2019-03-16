import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { MyProfilePage } from './my-profile';
import { ComponentsModule} from "../../components/components.module";

@NgModule({
  declarations: [
    MyProfilePage,
  ],
  imports: [
    ComponentsModule,
    IonicPageModule.forChild(MyProfilePage),
  ],
})
export class MyProfilePageModule {}
