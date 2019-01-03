import { Component } from '@angular/core';
import {IonicPage, MenuController, NavController, NavParams} from 'ionic-angular';


@IonicPage()
@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
})
export class LoginPage {

  constructor(public navCtrl: NavController, public navParams: NavParams , private menuCtrl :MenuController) {
  }


  onMenu(){
    this.menuCtrl.open();
  }

}
