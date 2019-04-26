import {Component, OnInit} from '@angular/core';
import {ListCardItem} from "../../models/list-card-item";
import {MyProfileService} from "../../services/my-profile.service";
import {ModalController, NavController} from "@ionic/angular";  
import { WishListComponent } from './components/wish-list/wish-list.component';
import { Router } from '@angular/router';

@Component({
    selector: 'app-my-profile',
    templateUrl: './my-profile.page.html',
    styleUrls: ['./my-profile.page.scss'],
})
export class MyProfilePage implements OnInit {
    profileImg: string = "assets/img/default_profile.png";
    profileListItems: ListCardItem [] = [];

    constructor(private profile: MyProfileService, public modalCtrl: ModalController,private router:Router,
        private navCtrl:NavController) {
            
    }

    ngOnInit() {
        if(!this.profile.isProfileLoaded){
            this.router.navigateByUrl('/dashboard');
        }
        this.profile.loadStudentSkills();
        this.profileImg = this.profile.getMyProfileImgPath()==undefined ? this.profileImg: this.profile.getMyProfileImgPath();
        
        this.profileListItems.push(new ListCardItem("Set your personal Data", "body", "create", "personalData"));
        this.profileListItems.push(new ListCardItem("Set your skills", "checkbox-outline", "create", "skills"));
        this.profileListItems.push(new ListCardItem("Wish List", "color-wand", "podium", "wishList"));
        this.profileListItems.push(new ListCardItem("My engagements", "mail", "done-all", "engagements"));
        //console.table(this.profileListItems.slice())
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
    onOpenSkills(){
        this.navCtrl.navigateForward('my-profile/skills');
    }
    async onOpenWishList(){
        const modal = await this.modalCtrl.create({
            component:WishListComponent
        });
        modal.present();
    }

    onOpenPersonalData() {
        this.navCtrl.navigateForward('my-profile/personal-data');
    }

    onOpenEngagements(){
        this.navCtrl.navigateForward('my-profile/engagements-list');
    }

    profileActivation(event:any){
        
        this.profile.isActiveProfile = event.detail.checked;
        this.profile.myProfile.active = event.detail.checked;
        this.profile.onUpdateProfileActivation();        
    }
}
