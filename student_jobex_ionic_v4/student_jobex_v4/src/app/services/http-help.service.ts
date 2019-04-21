import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ConfigService } from './config.service';

@Injectable({
  providedIn: 'root'
})
export class HttpHelpService {
  
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json',
      'Access-Control-Allow-Origin': '*'
    })}; 
  constructor(private http:HttpClient,private config:ConfigService) { 


  }
  submitForm(data:any,page:string){

    return this.http.post(this.config.getApiUrl()+page,data,this.httpOptions);
  }
}
