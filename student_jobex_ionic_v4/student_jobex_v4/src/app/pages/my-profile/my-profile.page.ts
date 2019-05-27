import {Component, OnInit} from '@angular/core';
import {ListCardItem} from "../../models/list-card-item";
import {MyProfileService} from "../../services/my-profile.service";
import {ModalController, NavController, LoadingController} from "@ionic/angular";  
import { WishListComponent } from './components/wish-list/wish-list.component';
import { Router } from '@angular/router';
import { MyProfile } from 'src/app/models/my-profile.model';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { load } from '@angular/core/src/render3';
import { Subscription } from 'rxjs';

@Component({
    selector: 'app-my-profile',
    templateUrl: './my-profile.page.html',
    styleUrls: ['./my-profile.page.scss'],
})
export class MyProfilePage implements OnInit {

    pLoadedSubject:Subscription;
    profileImg: string = "assets/img/default_profile.png";
    profileListItems: ListCardItem [] = [];
    myProfile:MyProfile;
    constructor(
        private profile: MyProfileService, 
        public modalCtrl: ModalController,
        private router:Router,
        private navCtrl:NavController,
        public loadingController: LoadingController,
        private auth:AuthenticationService) {
            
    }
  
    ngOnInit() {
        this.loadProfile();
    }

    async loadProfile(){
        const loading = await this.loadingController.create({
            message:"Setting Your profile"
        });
        loading.present();
        if(this.auth.isAuthenticated){
            if(!this.profile.myProfile){
                this.pLoadedSubject = this.profile.profileLoadedSubject.subscribe(
                    (value) => {
                        if(value == 'loaded'){
                            this.loadProfileLayout();
                            this.pLoadedSubject.unsubscribe();
                            loading.dismiss();
                        }
                    }
                );
                this.profile.loadProfile();
            }else{
                
                this.loadProfileLayout();
                loading.dismiss();
            }             
        }
    }
    onViewWillUnload(){
        if(this.pLoadedSubject){
          this.pLoadedSubject.unsubscribe();
        }
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
        this.navCtrl.navigateForward('my-profile/wish-list');
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
    
    loadProfileLayout(){
        this.myProfile = this.profile.myProfile;
        this.profileImg = this.profile.getMyProfileImgPath()==undefined ? this.profileImg: this.profile.getMyProfileImgPath();        
        this.profileListItems.push(new ListCardItem("Set your personal Data", "body", "create", "personalData"));
        this.profileListItems.push(new ListCardItem("Set your skills", "checkbox-outline", "create", "skills"));
        this.profileListItems.push(new ListCardItem("Wish List", "color-wand", "podium", "wishList"));
        this.profileListItems.push(new ListCardItem("My engagements", "mail", "done-all", "engagements"));
    }
}
