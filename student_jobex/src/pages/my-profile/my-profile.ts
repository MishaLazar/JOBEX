import { Component,OnInit } from '@angular/core';
import {IonicPage, MenuController, NavController} from 'ionic-angular';
import {MyProfileService} from "../../services/my-profile.service";

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

  constructor(public navCtrl: NavController,
              private menuCtrl:MenuController,private profileService:MyProfileService) {

  }

  ngOnInit(){

    if(this.profileService.isProfileImgSet()){
      this.profileImg = this.profileService.myProfile.profileImg;
    }
  }

  onMenuOpen(){
    this.menuCtrl.open();
  }
}
