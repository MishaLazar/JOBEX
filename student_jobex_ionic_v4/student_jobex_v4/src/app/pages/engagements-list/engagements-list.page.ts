import { Component, OnInit } from '@angular/core';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { Engagement } from 'src/app/models/engagement';
import { NavController } from '@ionic/angular';

@Component({
  selector: 'app-engagements-list',
  templateUrl: './engagements-list.page.html',
  styleUrls: ['./engagements-list.page.scss'],
})
export class EngagementsListPage implements OnInit {

  activeEngagements:Engagement[] = [];
  constructor(private sharedDataSvc:SharedDataService,private navCtrl:NavController) { }

  ngOnInit() {
    this.activeEngagements = this.sharedDataSvc.getStudentActiveEngagements();
  }
  openEngagment(matchId:string){
    this.navCtrl.navigateForward('my-profile/engagements-list/engagement/' + matchId);
  }
}
