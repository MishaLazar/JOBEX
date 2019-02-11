import {Injectable} from "@angular/core";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {StorageService} from "./storage.service";
import {ConfigService} from "./config.service";



@Injectable()
export class AuthenticationService {

  isAuthenticatedStatus:boolean = false;

  constructor(private http: HttpClient,private storageCtrl:StorageService,private config:ConfigService){}


  onSignin(username:string, password:string){

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Access-Control-Allow-Origin': '*'
      })};


   return this.http.post(this.config.getApiUrl()+'login',{username:username,password:password},httpOptions)


  }

  onLogout(){
    this.storageCtrl.removeItemByKey('access_token');
    this.storageCtrl.removeItemByKey('refresh_token');
  }

  isAuthenticated() {
    console.log('isAuthenticated :' + this.storageCtrl.getValueByKey('token'));
    return this.storageCtrl.getValueByKey('token') !== null;


  }
}
