import {Component, OnInit} from '@angular/core';
import {IonicPage, ModalController, NavController, NavParams} from 'ionic-angular';
import {MyProfileService} from "../../services/my-profile.service";

/**
 * Generated class for the PersonalDataPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-personal-data',
  templateUrl: 'personal-data.html',
})
export class PersonalDataPage implements  OnInit{
  profileImg: string = "assets/imgs/default_profile.png";

  constructor(public navCtrl: NavController, public navParams: NavParams,public profileService:MyProfileService,private modalCtrl:ModalController) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad PersonalDataPage');
  }

  ngOnInit(): void {
    if(this.profileService.isProfileImgSet()){
      this.profileImg = this.profileService.myProfile.profileImg;
    }
  }

  async closePersonalData(){
   //await this.modalCtrl.;

  }

}
