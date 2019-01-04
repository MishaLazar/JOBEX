import { Component } from '@angular/core';
import {IonicPage, MenuController, NavController, NavParams} from 'ionic-angular';
import {NgForm} from "@angular/forms";
import {AuthenticationService} from "../../services/authentication.service";

@IonicPage()
@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
})
export class LoginPage {

  constructor(public navCtrl: NavController,
              public navParams: NavParams ,
              private menuCtrl :MenuController,
              private authSrv:AuthenticationService) {
  }


  onMenu(){
    this.menuCtrl.open();
  }

  onSubmit(form: NgForm){

    this.authSrv.onSignin(form.value.email,form.value.password)
      .subscribe(data => {
        console.log(data);
      });

    console.log(form.value)
  }
}
