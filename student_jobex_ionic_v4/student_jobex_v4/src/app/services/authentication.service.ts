import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { ConfigService } from './config.service';
import { StorageService } from './storage.service';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor(private config:ConfigService,private http:HttpClient,private storage:StorageService) { }

  onSignin(username:string, password:string){

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Access-Control-Allow-Origin': '*'
      })};


   return this.http.post(this.config.getApiUrl()+'get_login',{username:username,password:password},httpOptions)


  }

  onLogout(){
    this.storage.removeItemByKey('access_token');
    this.storage.removeItemByKey('refresh_token');
  }

  isAuthenticated() {
    console.log('isAuthenticated :' + this.storage.getValueByKey('token'));
    return this.storage.getValueByKey('token') !== null;


  }
}
