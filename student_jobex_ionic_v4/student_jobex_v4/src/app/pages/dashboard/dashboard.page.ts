import { Component, OnInit } from '@angular/core';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { Engagement } from 'src/app/models/engagement';
import { NavController } from '@ionic/angular';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {


  studentLastEgagements:Engagement[];
  constructor(private sharedDataSvc:SharedDataService, private navCtrl:NavController) { }

  ngOnInit() {
    this.studentLastEgagements = this.sharedDataSvc.getStudentEngagments();
    console.log(this.studentLastEgagements);
  }

  onClickTest(mid:string){
    this.navCtrl.navigateForward('dashboard/engagement/'+mid);
  }

}
