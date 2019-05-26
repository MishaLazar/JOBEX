import { PipeTransform, Pipe, OnInit } from '@angular/core';
import { City } from '../models/City';

@Pipe({
    name: 'CitiesFilter'
  })
  export class CitiesFilterPipe implements PipeTransform {

    constructor(){
      
    }
    transform(value: City[], city: string) {
      if (city !== undefined && city.length >= 2) {
        city = city.toLowerCase();        
        return value.filter(function(el: any) {                            
          return el["city_desc"].toLowerCase().indexOf(city) > -1;
        });
      }
      return [];
    }
  }