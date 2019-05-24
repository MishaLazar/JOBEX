import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
import { StatusBar } from '@ionic-native/status-bar/ngx';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import {AuthenticationService} from "./services/authentication.service";
import {ConfigService} from "./services/config.service";
import {MyProfileService} from "./services/my-profile.service";
import {StorageService} from "./services/storage.service";
import {ProfileComponentsModule} from "./pages/my-profile/components/profile-componentsModule";
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { SharedDataService } from './services/shared-data.service';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { RefreshTokenInterceptor } from './Utils/RefreshTokenInterceptor';

@NgModule({
  declarations: [AppComponent],
  entryComponents: [],
  imports: [
    BrowserModule, 
    IonicModule.forRoot(), 
    AppRoutingModule,
    
    HttpClientModule,    
    ReactiveFormsModule,
    ProfileComponentsModule
  ],
  providers: [
    StatusBar,
    SplashScreen,
      AuthenticationService,
      ConfigService,
      StorageService,
      MyProfileService,
      SharedDataService,
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: RefreshTokenInterceptor,
      multi: true
    }
  ],
  exports:[
    ReactiveFormsModule,FormsModule,
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
