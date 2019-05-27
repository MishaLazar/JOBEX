import { Component } from '@angular/core';

import { Platform, NavController } from '@ionic/angular';
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
import { StatusBar } from '@ionic-native/status-bar/ngx';
import {MenuItem} from "./models/menu-item";
import { StorageService } from './services/storage.service';
import { Router } from '@angular/router';
import { AuthenticationService } from './services/authentication.service';
import { MyProfileService } from './services/my-profile.service';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html'
})
export class AppComponent {
  public appMenu=[
      new MenuItem("Dashboard","/dashboard","clipboard"),
      //new MenuItem("Register","/register","create"),      
      new MenuItem("My Profile","/my-profile","person")
      
      //new MenuItem("Logout","/logout","log-in")
      
  ];
  isAuthenticated:boolean = false;
  constructor(
    private platform: Platform,
    private splashScreen: SplashScreen,
    private statusBar: StatusBar,
    private router:Router,
    private auth:AuthenticationService,
    private storage:StorageService,
    private profile:MyProfileService
  ) {
    
    this.isAuthenticated = this.auth.isAuthenticated();
    this.initializeApp();
    if(!this.isAuthenticated){
      this.router.navigateByUrl('/login');
    }
      
    
    
  }

  initializeApp() {
    this.platform.ready().then(() => {
      this.statusBar.styleDefault();
      this.splashScreen.hide();
      this.auth.stateSubject.subscribe((value) =>{
        if(value='login'){
          this.isAuthenticated = true;
        }else{
          
          this.isAuthenticated = false;
          this.router.navigateByUrl('/login');
        }
       
      }
      )
    });
  }
  onLogout(){
    
    this.storage.logout();
    this.auth.onLogout();
    this.router.navigateByUrl('/login');
  }
}
