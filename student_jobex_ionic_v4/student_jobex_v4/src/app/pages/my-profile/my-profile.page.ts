import {Component, OnInit} from '@angular/core';
import {ListCardItem} from "../../models/list-card-item";
import {MyProfileService} from "../../services/my-profile.service";
import {ModalController, NavController} from "@ionic/angular";
import {PersonalDataComponent} from "./components/personal-data/personal-data.component";
import { EngagementsComponent } from './components/engagements/engagements.component';
import { SkillsComponent } from './components/skills/skills.component';
import { WishListComponent } from './components/wish-list/wish-list.component';

@Component({
    selector: 'app-my-profile',
    templateUrl: './my-profile.page.html',
    styleUrls: ['./my-profile.page.scss'],
})
export class MyProfilePage implements OnInit {
    profileImg: string = "assets/img/default_profile.png";
    profileListItems: ListCardItem [] = [];

    constructor(private profileService: MyProfileService, public modalCtrl: ModalController,
        private navCtrl:NavController) {
    }

    ngOnInit() {
        if (this.profileService.isProfileImgSet()) {
            this.profileImg = this.profileService.myProfile.profileImg;
        }
        this.profileListItems.push(new ListCardItem("Set your personal Data", "body", "create", "personalData"));
        this.profileListItems.push(new ListCardItem("Set your skills", "checkbox-outline", "create", "skills"));
        this.profileListItems.push(new ListCardItem("Wish List", "color-wand", "podium", "wishList"));
        this.profileListItems.push(new ListCardItem("My engagements", "mail", "done-all", "engagements"));
        console.table(this.profileListItems.slice())
    }

    onItemClick(cardId: string) {
        switch (cardId) {
            case "personalData":
                this.onOpenPersonalData();
                break;
            case "engagements":
                this.onOpenEngagements();
                break;
            case "wishList":
                this.onOpenWishList();
                break;
            case "skills":
                this.onOpenSkills();
                break;
        }
    }
    async onOpenSkills(){
        const modal = await this.modalCtrl.create({
            component:SkillsComponent
        });
        modal.present();
    }
    async onOpenWishList(){
        const modal = await this.modalCtrl.create({
            component:WishListComponent
        });
        modal.present();
    }

    async onOpenPersonalData() {
        const modal = await this.modalCtrl.create({
            component:PersonalDataComponent,
            componentProps: { value: 123 }
        });

        return await modal.present();
    }

    onOpenEngagements(){
        this.navCtrl.navigateForward('my-profile/engagements-list')
    }
}
