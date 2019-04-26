import { Component, OnInit } from '@angular/core';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { Engagement } from 'src/app/models/engagement';
import { NavController } from '@ionic/angular';
import { MyProfileService } from 'src/app/services/my-profile.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {


  studentLastEgagements:Engagement[];
  constructor(private sharedDataSvc:SharedDataService, private navCtrl:NavController,private profile:MyProfileService) { }

  ngOnInit() {
     
    
    if(!this.profile.isProfileLoaded){
      this.profile.loadProfile();
    }
    this.studentLastEgagements = this.sharedDataSvc.getStudentLatestEngagments();

    this.sharedDataSvc.loadAllSkills();
  }

  // onClickTest(mid:string){
  //   this.navCtrl.navigateForward('dashboard/engagement/'+mid);
  // }
  onClick(){
    this.profile.loadStudentSkills();
  }
}
