import {Injectable} from "@angular/core";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {StorageService} from "./storage.service";



@Injectable()
export class AuthenticationService {

  api_url = 'http://127.0.0.1:5050/';
  isAuthenticatedStatus:boolean = false;

  constructor(private http: HttpClient,private storageCtrl:StorageService){}


  onSignin(username:string, password:string){

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Access-Control-Allow-Origin': '*'
      })};


   return this.http.post(this.api_url+'login',{username:username,password:password},httpOptions)


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
