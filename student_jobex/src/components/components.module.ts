import { NgModule } from '@angular/core';
import { ListItemCardComponent } from './list-item-card/list-item-card';
import {IonicModule} from "ionic-angular";
@NgModule({
	declarations: [ListItemCardComponent],
	imports: [IonicModule],
	exports: [ListItemCardComponent]
})
export class ComponentsModule {}
