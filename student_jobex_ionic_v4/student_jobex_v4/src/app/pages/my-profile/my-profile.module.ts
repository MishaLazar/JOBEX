import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {Routes, RouterModule} from '@angular/router';

import {IonicModule} from '@ionic/angular';

import {MyProfilePage} from './my-profile.page';
import {PersonalDataComponent} from "./components/personal-data/personal-data.component";
import {ListCardItemComponent} from "./components/list-card-item/list-card-item.component";
import { EngagementsComponent } from './components/engagements/engagements.component';
import { ProfileComponentsModule } from './components/profile-componentsModule';
import { WishListComponent } from './components/wish-list/wish-list.component';
import { SkillsComponent } from './components/skills/skills.component';


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
    entryComponents: [PersonalDataComponent,ListCardItemComponent,EngagementsComponent,WishListComponent,SkillsComponent]
})
export class MyProfilePageModule {
}
