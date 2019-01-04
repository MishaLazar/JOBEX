import {Injectable} from "@angular/core";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {catchError} from "rxjs/operators";


@Injectable()
export class AuthenticationService {

  constructor(private http: HttpClient){}

  api_url = 'http://127.0.0.1:5050/';

  onSignin(username:string, password:string){

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Access-Control-Allow-Origin': '*'
      })};


   return this.http.post(this.api_url+'login',{username:username,password:password},httpOptions)


  }

}
