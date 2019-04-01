import { NgModule } from '@angular/core';
import {PersonalDataComponent} from "./personal-data/personal-data.component";
import {IonicModule} from "@ionic/angular";
import {ListCardItemComponent} from "./list-card-item/list-card-item.component";
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@NgModule({
    declarations: [ListCardItemComponent,PersonalDataComponent],
    imports: [IonicModule,FormsModule,ReactiveFormsModule],
    exports: [ListCardItemComponent],
    entryComponents:[PersonalDataComponent]
})

export class ProfileComponentsModule {}