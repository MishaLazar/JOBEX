import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { ConfigService } from './config.service';
import { StorageService } from './storage.service';
import { HttpHelpService } from './http-help.service';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor(private http:HttpHelpService,private storage:StorageService) { }

  onSignin(username:string, password:string){
    return this.http.submitForm({username:username,password:password},'get_login');

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
