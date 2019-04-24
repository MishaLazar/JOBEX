import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ConfigService } from './config.service';
import { StorageService } from './storage.service';

@Injectable({
  providedIn: 'root'
})
export class HttpHelpService {
  
  
  constructor(private http:HttpClient,private config:ConfigService,private storage:StorageService) { 


  }
  submitForm(data:any,page:string){
    const httpOptions = this.headers();
    
    return this.http.post(this.config.getApiUrl()+page,data,httpOptions);
  }

  get(page:string){
    const httpOptions = this.headers();
    return this.http.get(this.config.getApiUrl() + page,httpOptions);
  }
  
  refreshToken(page: string) {
    const refreshOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authorization': `Bearer ${this.storage.getRefreshToken()}`
      })};

      return this.http.post(this.config.getApiUrl()+page , null,refreshOptions)
    }
    
  
  headers(){
    return {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authorization': `Bearer ${this.storage.getToken()}`
      })};
  }
}
