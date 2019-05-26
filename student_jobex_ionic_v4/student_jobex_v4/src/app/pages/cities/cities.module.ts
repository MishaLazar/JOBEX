import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { CitiesPage } from './cities.page';
import { CitiesFilterPipe } from 'src/app/filters/CitiesFilter';

const routes: Routes = [
  {
    path: '',
    component: CitiesPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  declarations: [CitiesPage,CitiesFilterPipe]
})
export class CitiesPageModule {}
