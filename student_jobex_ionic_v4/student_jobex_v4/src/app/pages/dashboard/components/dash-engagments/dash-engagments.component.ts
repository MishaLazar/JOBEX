import { Component, OnInit, Input } from '@angular/core';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { ConfigService } from 'src/app/services/config.service';
import { NavController } from '@ionic/angular';
import { Engagement } from 'src/app/models/engagement';

@Component({
  selector: 'dash-engagments',
  templateUrl: './dash-engagments.component.html',
  styleUrls: ['./dash-engagments.component.scss'],
})
export class DashEngagmentsComponent implements OnInit {

  engagements:Engagement[];
  constructor(
    private profile:MyProfileService,
    private config:ConfigService,    
    private navCtrl:NavController) {

    
   }

  ngOnInit() {
    this.loadEngagements();
  }

  async loadEngagements(){
    // const loading = await this.loadingController.create();
    // loading.present();

    this.profile.loadLatestsEngagements(this.config.getMaxNumOfLatests()).subscribe(
      (data:Engagement[]) => {
        this.engagements = data;
        
        // loading.dismiss();
      },
      (error) => {
        console.log(error);
        // loading.dismiss();
      }
    );
  }

  onEngagmentClick(match_id:string){
    console.log(match_id);
    this.navCtrl.navigateForward('dashboard/engagement/'+match_id);
  }
}
