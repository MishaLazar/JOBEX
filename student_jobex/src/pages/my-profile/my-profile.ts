import { Component,OnInit } from '@angular/core';
import {IonicPage,  MenuController, NavController} from 'ionic-angular';
import {MyProfileService} from "../../services/my-profile.service";
import {ListCardItem} from "../../models/list-card-item";


/**
 * Generated class for the MyProfilePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-my-profile',
  templateUrl: 'my-profile.html',
})
export class MyProfilePage implements OnInit {
  profileImg: string = "assets/imgs/default_profile.png";
  profileListItems:ListCardItem [] = [];

  constructor(public navCtrl: NavController,
              private menuCtrl:MenuController,private profileService:MyProfileService) {


  }

  ngOnInit(){

    if(this.profileService.isProfileImgSet()){
      this.profileImg = this.profileService.myProfile.profileImg;
    }
    this.profileListItems.push(new ListCardItem("Set your personal Data","body","create"));
    this.profileListItems.push(new ListCardItem("Set your skills","checkbox-outline","create"));
    console.table(this.profileListItems.slice())
  }

  onMenuOpen(){
    this.menuCtrl.open();
  }

}
