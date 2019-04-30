import {Component, OnInit} from '@angular/core';
import {ListCardItem} from "../../models/list-card-item";
import {MyProfileService} from "../../services/my-profile.service";
import {ModalController, NavController} from "@ionic/angular";  
import { WishListComponent } from './components/wish-list/wish-list.component';
import { Router } from '@angular/router';
import { MyProfile } from 'src/app/models/my-profile.model';
import { AuthenticationService } from 'src/app/services/authentication.service';

@Component({
    selector: 'app-my-profile',
    templateUrl: './my-profile.page.html',
    styleUrls: ['./my-profile.page.scss'],
})
export class MyProfilePage implements OnInit {
    profileImg: string = "assets/img/default_profile.png";
    profileListItems: ListCardItem [] = [];
    myProfile:MyProfile;
    constructor(private profile: MyProfileService, public modalCtrl: ModalController,private router:Router,
        private navCtrl:NavController,private auth:AuthenticationService) {
            
    }

    ngOnInit() {
        
        if(this.auth.isAuthenticated){
            if(!this.profile.myProfile){
                
                this.profile.profileLoadedSubject.subscribe(
                    (value) => {
                        if(value == 'loaded'){
                            this.loadProfileLayout();
                        }
                    }
                );
                this.profile.loadProfile();
            }else{
                this.loadProfileLayout();
            }            
        }
        
        
        
        //this.profile.loadStudentSkills();
       
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
