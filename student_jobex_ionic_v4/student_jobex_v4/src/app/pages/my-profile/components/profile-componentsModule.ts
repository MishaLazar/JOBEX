import { NgModule } from '@angular/core';
import {PersonalDataComponent} from "./personal-data/personal-data.component";
import {IonicModule} from "@ionic/angular";
import {ListCardItemComponent} from "./list-card-item/list-card-item.component";
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { EngagementsComponent } from './engagements/engagements.component';
import { SkillsComponent } from './skills/skills.component';
import { WishListComponent } from './wish-list/wish-list.component';
import { CommonModule } from '@angular/common';


@NgModule({
    declarations: [ListCardItemComponent,PersonalDataComponent,EngagementsComponent,SkillsComponent,WishListComponent],
    imports: [IonicModule,CommonModule,FormsModule,ReactiveFormsModule],
    exports: [ListCardItemComponent],
    entryComponents:[PersonalDataComponent,EngagementsComponent,WishListComponent,SkillsComponent]
})

export class ProfileComponentsModule {}