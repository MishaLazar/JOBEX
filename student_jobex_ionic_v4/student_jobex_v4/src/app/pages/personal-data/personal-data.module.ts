import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { PersonalDataPage } from './personal-data.page';


const routes: Routes = [
  {
    path: '',
    component: PersonalDataPage
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes),
    
    CommonModule,
    ReactiveFormsModule,
    IonicModule     
    
  ],
  declarations: [PersonalDataPage],
  
  
})
export class PersonalDataPageModule {}
