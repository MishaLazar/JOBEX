import { Component, OnInit, OnDestroy } from '@angular/core';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { PositionData } from 'src/app/models/position-data';
import { LoadingController } from '@ionic/angular';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'dash-chart-best4you',
  templateUrl: './dash-chart-best4you.component.html',
  styleUrls: ['./dash-chart-best4you.component.scss'],
})
export class DashChartBest4youComponent implements OnInit,OnDestroy {

  wLSubject: Subscription;
  sLoadedSubject: Subscription;
  skill_id: number;
  skill_text_value: string;
  skill_diff: any;
  pLoadedSubject: Subscription;
  refreshSubsciprtion: Subscription;

  constructor(private profile: MyProfileService, private loadingController: LoadingController, private sharedData: SharedDataService) {

  }

  ngOnInit() {
    if (!this.sharedData.skills) {
      this.sLoadedSubject = this.sharedData.skillsLoadedSubject.subscribe(
        (value) => {
          if (value == 'loaded') {
            this.loadWishListSuggestedSkill();
            this.sLoadedSubject.unsubscribe();
          }
        }
      );
      this.sharedData.loadAllSkills();
    }
    else {

      this.loadWishListSuggestedSkill();
    }

    this.refreshSubsciprtion = this.profile.refresherSubject.subscribe((value) =>{
      this.skill_id = undefined;
      this.profile.wl_suggested = undefined;
      this.doLoadSuggestedSkill()
      
    })

  }
  ngOnDestroy(): void {
    this.refreshSubsciprtion.unsubscribe();
  }
  ionViewWillEnter() {
    this.loadWishListSuggestedSkill();

  }
  loadWishListSuggestedSkill() {
    if (!this.profile.myProfile) {
      this.pLoadedSubject = this.profile.profileLoadedSubject.subscribe((value) => {
        if (value == 'loaded') {
          this.pLoadedSubject.unsubscribe();
          this.doLoadSuggestedSkill();
        }
      });
    } else {
      this.doLoadSuggestedSkill();
    }

  }
  onViewWillUnload() {
    if (this.pLoadedSubject) {
      this.pLoadedSubject.unsubscribe();
    }

    if (this.sLoadedSubject) {
      this.sLoadedSubject.unsubscribe();
    }

    if(this.wLSubject){
      this.wLSubject.unsubscribe();
    }
  }

  doLoadSuggestedSkill() {
    if (!this.profile.wl_suggested) {
      this.wLSubject = this.profile.WL_SuggestedSubject.subscribe(
        (status: string) => {
          if (status === 'success') {
            this.skill_id = this.profile.wl_suggested.new_skill_skill_id;
            this.skill_text_value = this.sharedData.getSkillTextValueById(this.skill_id);
            this.skill_diff = (this.profile.wl_suggested.diff * 100).toFixed(2);
            this.wLSubject.unsubscribe();
          } else {
            console.log("error loading studend skills");
          }

        }
      );
      this.profile.calculateWishlistSggestedSkill();
    } else {
      this.skill_id = this.profile.wl_suggested.new_skill_skill_id;
      this.skill_text_value = this.sharedData.getSkillTextValueById(this.skill_id);
    }
  }
}
