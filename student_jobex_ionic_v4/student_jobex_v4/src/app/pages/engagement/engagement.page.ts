import { Component, OnInit, Input } from '@angular/core';
import { Engagement } from 'src/app/models/engagement';
import { ActivatedRoute } from '@angular/router';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { LoadingController } from '@ionic/angular';
import { HttpHelpService } from 'src/app/services/http-help.service';
import { MyProfileService } from 'src/app/services/my-profile.service';

@Component({
  selector: 'app-engagement',
  templateUrl: './engagement.page.html',
  styleUrls: ['./engagement.page.scss'],
})
export class EngagementPage implements OnInit {

  match_id:string;    
  engagement:Engagement = null;
  constructor(private activateRoute:ActivatedRoute,private profile:MyProfileService,private loadingController: LoadingController,
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
        loading.dismiss();
      },
      (error) =>{
        
        loading.dismiss();
      }
      
    )
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
}
