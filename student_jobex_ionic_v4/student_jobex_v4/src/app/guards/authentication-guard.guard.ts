import { Injectable } from '@angular/core';
import { CanLoad, Route, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthenticationService } from '../services/authentication.service';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationGuardGuard implements  CanLoad{

  constructor(private auth:AuthenticationService, private router:Router){

  }
  canLoad(route:Route, segments: import("@angular/router").UrlSegment[]): boolean | Observable<boolean> | Promise<boolean> {
    console.log("is authenticated:"+ this.auth.isAuthenticated());
    if(!this.auth.isAuthenticated()){
     
      
      this.router.navigateByUrl('/login')
    }
    return this.auth.isAuthenticated();
  }
  
}
