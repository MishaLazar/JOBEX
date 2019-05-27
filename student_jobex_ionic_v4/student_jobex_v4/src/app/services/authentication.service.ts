import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { ConfigService } from './config.service';
import { StorageService } from './storage.service';
import { HttpHelpService } from './http-help.service';
import { Subject } from 'rxjs';
import { MyProfileService } from './my-profile.service';
import { RefreshTokenInterceptor } from '../Utils/RefreshTokenInterceptor';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
    
  

  public stateSubject = new Subject();
  private isAuthenticatedStudent:boolean = false;
  constructor(private http:HttpHelpService,private storage:StorageService,private profile:MyProfileService) { 

  }


  onSignin(username:string, password:string){
    
    return this.http.submitForm({username:username,password:password},'get_login');

  }

  onLogout(){
    
    this.storage.logout();
    this.stateSubject.next('logout');
  }

  isAuthenticated() {
    
    return this.storage.getValueByKey('access_token') !== null;


  }
 
  setRefreshedToken(token:string){
    this.storage.setStorageValueByKey('access_token',token)
  }

  getToken() {
    return this.storage.getValueByKey('access_token');
  }
  
  refreshAccessToken(): any {
    return this.http.refreshToken('tokenRefresh');
  }

  setUserIdFromStorage(): any {
    this.profile.setUserIdOnLogin(this.storage.getUserId());
  }


}
