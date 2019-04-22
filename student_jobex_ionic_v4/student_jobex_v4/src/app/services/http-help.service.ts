import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ConfigService } from './config.service';
import { AuthenticationService } from './authentication.service';
import { StorageService } from './storage.service';

@Injectable({
  providedIn: 'root'
})
export class HttpHelpService {
  
  
  constructor(private http:HttpClient,private config:ConfigService,private storage:StorageService) { 


  }
  submitForm(data:any,page:string){
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authorization': `Bearer ${this.storage.getToken()}`
      })};
    debugger;
    return this.http.post(this.config.getApiUrl()+page,data,httpOptions);
  }
}
