import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  

  private api_url = 'http://10.100.102.6:5050/';
  constructor() { }  


  getApiUrl(){
    return this.api_url;
  }
  getMaxNumOfLatests(): 3 {
    return 3;
  }
}
