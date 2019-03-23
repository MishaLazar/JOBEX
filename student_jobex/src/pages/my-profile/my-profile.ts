import {Component, OnInit} from '@angular/core';
import {IonicPage, MenuController, ModalController, NavController} from 'ionic-angular';
import {MyProfileService} from "../../services/my-profile.service";
import {ListCardItem} from "../../models/list-card-item";
import {PersonalDataComponent} from "../../components/personal-data/personal-data";

@IonicPage()
@Component({
  selector: 'page-my-profile',
  templateUrl: 'my-profile.html',

})
export class MyProfilePage implements OnInit {
  profileImg: string = "assets/imgs/default_profile.png";
  profileListItems: ListCardItem [] = [];

  constructor(public navCtrl: NavController,
              private menuCtrl: MenuController, private profileService: MyProfileService, public modalCtrl: ModalController) {


  }

  ngOnInit() {

    if (this.profileService.isProfileImgSet()) {
      this.profileImg = this.profileService.myProfile.profileImg;
    }
    this.profileListItems.push(new ListCardItem("Set your personal Data", "body", "create", "personalData"));
    this.profileListItems.push(new ListCardItem("Set your skills", "checkbox-outline", "create", "skills"));
    this.profileListItems.push(new ListCardItem("Best for you", "color-wand", "podium", "best"));
    this.profileListItems.push(new ListCardItem("My engagements", "mail", "done-all", "engagements"));
    console.table(this.profileListItems.slice())
  }

  onMenuOpen() {
    this.menuCtrl.open();
  }

  onItemClick(cardId: string) {
    switch (cardId) {
      case "personalData":
        this.onOpenPersonnalData();
        break;
    }
  }

  async onOpenPersonnalData() {
    console.log("1");
    const modal = await this.modalCtrl.create(PersonalDataComponent, { value: 123 });

    return await modal.present();


  }
}
