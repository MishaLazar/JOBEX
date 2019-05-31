import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  

  private api_url = 'http://192.168.43.4:5050/';
  constructor() { }  


  getApiUrl(){
    return this.api_url;
  }
  getMaxNumOfLatests(): 3 {
    return 3;
  }
}
