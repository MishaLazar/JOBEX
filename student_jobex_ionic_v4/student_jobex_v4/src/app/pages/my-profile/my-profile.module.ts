import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {Routes, RouterModule} from '@angular/router';

import {IonicModule} from '@ionic/angular';

import {MyProfilePage} from './my-profile.page';
import {PersonalDataComponent} from "./components/personal-data/personal-data.component";
import {ListCardItemComponent} from "./components/list-card-item/list-card-item.component";
import {ProfileComponentsModule} from "./components/profile-componentsModule";

const routes: Routes = [
    {
        path: '',
        component: MyProfilePage
    }
];

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        IonicModule,
        ProfileComponentsModule,
        RouterModule.forChild(routes)
    ],
    declarations: [MyProfilePage],
    entryComponents: [PersonalDataComponent,ListCardItemComponent]
})
export class MyProfilePageModule {
}
