import { Component } from '@angular/core';
import {IonicPage, LoadingController, MenuController, NavController, NavParams} from 'ionic-angular';
import {NgForm} from "@angular/forms";
import {AuthenticationService} from "../../services/authentication.service";
import {Token} from "../../models/token.model";
import {StorageService} from "../../services/storage.service";
import {HomePage} from "../home/home";


@IonicPage()
@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
})
export class LoginPage {

  constructor(public navCtrl: NavController,
              public navParams: NavParams ,
              private menuCtrl :MenuController,
              private authSrv:AuthenticationService,
              private storeSrv: StorageService,
              private loadingCtrl:LoadingController
  ) {
  }


  onMenuOpen(){
    this.menuCtrl.open();
  }

  onSubmit(form: NgForm){
    const loading = this.loadingCtrl.create({
      content:'Signing you up...'
    });
    loading.present();
    this.authSrv.onSignin(form.value.email,form.value.password)
      .subscribe((data:Token) => {
        loading.dismiss();
        this.storeSrv.setStorageValueByKey('access_token',data.access_token);
        this.storeSrv.setStorageValueByKey('refresh_token',data.refresh_token);
        this.navCtrl.setRoot(HomePage);
      });
  }
}
