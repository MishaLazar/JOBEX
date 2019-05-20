import { Component, OnInit, Input } from '@angular/core';
import { Engagement } from 'src/app/models/engagement';
import { ActivatedRoute } from '@angular/router';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { LoadingController, AlertController, ToastController } from '@ionic/angular';
import { HttpHelpService } from 'src/app/services/http-help.service';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { SkillList } from 'src/app/models/student_skill';

@Component({
  selector: 'app-engagement',
  templateUrl: './engagement.page.html',
  styleUrls: ['./engagement.page.scss'],
})
export class EngagementPage implements OnInit {

  match_id:string;  
  shownSection:any;  
  engagement:Engagement = null;
  positionSkills: SkillList[];
  skillsToDisplay:String[] = [];
  constructor(
    private activateRoute:ActivatedRoute,
    private profile:MyProfileService,
    private loadingController: LoadingController,
    private sharedData:SharedDataService,
    private alertController:AlertController,
    private toastController:ToastController,
    private http:HttpHelpService) {

   }

  ngOnInit() {
    
    this.match_id = this.activateRoute.snapshot.paramMap.get('matchId');
    this.loadEngagmentByMatchId();    
    // this.engagement = this.sharedDateSvc.getStudentLatestEngagmentByMatchId(this.matchId);
  }

  async loadEngagmentByMatchId(){
    const loading = await this.loadingController.create(
      {
        message:"loading ..."
      }
      );
    loading.present();
    let data = {
      student_id:this.profile.user_id,
      match_id:this.match_id  
    }

    this.http.submitForm(data,'student/get_student_engagement_by_match').subscribe(
      (data:Engagement) => {
        this.engagement = data;
        if(this.engagement.is_new){
          this.setEngagementIsOpened();
        }     
        this.toggleSection('position_description');
        
        this.setPositionSkills();
        this.presentFeedbackPrompt();
        loading.dismiss();
      },
      (error) =>{
        
        loading.dismiss();
      }
      
    )
  }

  setPositionSkills(){    
    let tempSkillsFlat:number[] = [];
    let skills = this.sharedData.skills.slice();
    this.positionSkills = this.engagement.position_skill_list.slice();
    this.positionSkills.forEach(positionSkill => 
      positionSkill.skills.forEach(skill =>
        tempSkillsFlat.push(skill.skill_Id)
      )
    );
    tempSkillsFlat.forEach(skill =>
      {
        
        let index = skills.findIndex(
          el => el.SkillId === Number(skill));
        if(index >= 0){
          
          this.skillsToDisplay.push(this.sharedData.skills[index].TextValue);
        }
      }
    );      
     
  }

  setEngagementIsOpened(){
    let data = {
      student_id:this.profile.user_id,
      engagement_id:this.engagement._id,
      update_fields:{
        is_new:false
      }
    }

    this.http.submitForm(data,'student/engagement_update').subscribe(
      (success:any) =>{
        console.log(success);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  toggleSection(section) {
    if (this.isShownSection(section)) {
      this.shownSection = null;
    } else {
      this.shownSection = section;
    }
    // $ionicScrollDelegate.resize();
  }


  isShownSection(section) {
    return this.shownSection === section;
  }

  
  async presentFeedbackPrompt() {
    const alert = await this.alertController.create({
      header: 'feedback',
      inputs: [
        {
          name: 'feedback_text',
          type: 'text',
          placeholder: 'Enter Your Feedback Please'
        }
      ],
      buttons: [
        {
          text: 'No Thanks!',
          role: 'cancel',
          cssClass: 'secondary',
          handler: ()  => {
            let data = {
              feedback_text:"",
              engagement_id:this.engagement._id,
              company_id:this.engagement.company_id,
              status:true
            }
            this.http.submitForm(data,'engagement/feedback').subscribe(
              (success:any) =>{
                this.toastController.create({
                  message:"Thanks",
                  duration:500
                })
              },
              (error) => {
                console.log(error);
              }
            );
          }
        }, {
          text: 'Submit',
          handler: feedback => {            
            let data = {
              feedback_text:feedback["feedback_text"],
              engagement_id:this.engagement._id,
              company_id:this.engagement.company_id,
              status:true
            }
            this.http.submitForm(data,'engagement/feedback').subscribe(
              (success:any) =>{
                this.toastController.create({
                  message:"Thanks",
                  duration:500
                })
              },
              (error) => {
                console.log(error);
              }
            );
          }
        }
      ]
    });

    await alert.present();
  }

}
