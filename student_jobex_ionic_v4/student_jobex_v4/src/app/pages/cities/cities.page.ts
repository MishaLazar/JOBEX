import { Component, OnInit } from '@angular/core';
import { City } from 'src/app/models/City';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { LoadingController } from '@ionic/angular';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { Location } from '@angular/common';
@Component({
  selector: 'app-cities',
  templateUrl: './cities.page.html',
  styleUrls: ['./cities.page.scss'],
})
export class CitiesPage implements OnInit {

  CitySearchTerm:any;
  Cities:City[];
  City:City;
  constructor(public sharedData:SharedDataService,public loading:LoadingController,public profile:MyProfileService,public location:Location) { }

  ngOnInit() {

    if(!this.sharedData.cities){
      this.loadCities();
    }else{
      this.Cities = this.sharedData.cities.slice();
    }
  }

  async loadCities(){

    const loading = await this.loading.create({
      message:"loading cities list"
    });
    loading.present();
    this.sharedData.citiesLoadedSubject.subscribe((value) =>{
      if(value='loaded'){
        this.Cities = this.sharedData.cities.slice();
      }else{
        console.error('Opps!');
      }
      loading.dismiss();
    }            
    );
    this.sharedData.loadAllCities();

  }
  termChange(term:any){
    
    this.CitySearchTerm = term.srcElement.value;
  }
  CityTuched(city:City){
    this.profile.myProfile.address = city.city_desc;
    this.profile.myProfile.location = city.city_id;
    this.location.back();
  }
}
