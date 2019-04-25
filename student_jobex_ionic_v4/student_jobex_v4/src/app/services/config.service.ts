import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  

  private api_url = 'http://127.0.0.1:5050/';
  constructor() { }  


  getApiUrl(){
    return this.api_url;
  }
  getMaxNumOfLatests(): 3 {
    return 3;
  }
}
