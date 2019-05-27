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
    
    if(!this.auth.isAuthenticated()){
     
      
      this.router.navigateByUrl('/login')
    }
    this.auth.setUserIdFromStorage();
    return this.auth.isAuthenticated();
  }
  
}
