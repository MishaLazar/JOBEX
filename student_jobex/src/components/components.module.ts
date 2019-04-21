import { NgModule } from '@angular/core';
import { ListItemCardComponent } from './list-item-card/list-item-card';
import {IonicModule} from "ionic-angular";
import {PersonalDataComponent} from "./personal-data/personal-data";


@NgModule({
	declarations: [ListItemCardComponent,PersonalDataComponent],
	imports: [IonicModule],
	exports: [ListItemCardComponent],
  entryComponents:[PersonalDataComponent]
})
export class ComponentsModule {}
