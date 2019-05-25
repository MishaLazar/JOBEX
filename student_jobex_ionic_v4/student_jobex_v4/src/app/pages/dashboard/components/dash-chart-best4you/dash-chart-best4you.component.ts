import { Component, OnInit } from '@angular/core';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { PositionData } from 'src/app/models/position-data';
import { LoadingController } from '@ionic/angular';
import { SharedDataService } from 'src/app/services/shared-data.service';

@Component({
  selector: 'dash-chart-best4you',
  templateUrl: './dash-chart-best4you.component.html',
  styleUrls: ['./dash-chart-best4you.component.scss'],
})
export class DashChartBest4youComponent implements OnInit {

  
  
  skill_id:number;
  skill_text_value:string;
  skill_diff:any;

  constructor(private profile:MyProfileService,private loadingController:LoadingController, private sharedData:SharedDataService) { 
    
  }

  ngOnInit() {
    if(!this.sharedData.skills){
      this.sharedData.skillsLoadedSubject.subscribe(
        (value) => {
          if(value =='loaded'){
            this.loadWishListSuggestedSkill();
            this.sharedData.skillsLoadedSubject.unsubscribe();
          }
        }
      );
      this.sharedData.loadAllSkills();
    }
    else{

      this.loadWishListSuggestedSkill();
    }
    
  }

  ionViewWillEnter(){
    this.loadWishListSuggestedSkill();
  }
  loadWishListSuggestedSkill() {
    if(!this.profile.wl_suggested){
      this.profile.WL_SuggestedSubject.subscribe(
        (status:string) =>{
          if(status === 'success'){         
            this.skill_id = this.profile.wl_suggested.new_skill_skill_id;
            this.skill_text_value = this.sharedData.getSkillTextValueById(this.skill_id);
            this.skill_diff = (this.profile.wl_suggested.diff * 100).toFixed(2);
            
          }else{
            console.log("error loading studend skills");
          }    
          this.profile.WL_SuggestedSubject.unsubscribe();    
        }
      );
      this.profile.calculateWishlistSggestedSkill();
    }else {
      this.skill_id = this.profile.wl_suggested.new_skill_skill_id;
      this.skill_text_value = this.sharedData.getSkillTextValueById(this.skill_id);
    }

  }

}
