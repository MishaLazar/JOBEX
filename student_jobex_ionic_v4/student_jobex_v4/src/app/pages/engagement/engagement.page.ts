import { Component, OnInit, Input } from '@angular/core';
import { Engagement } from 'src/app/models/engagement';
import { ActivatedRoute } from '@angular/router';
import { SharedDataService } from 'src/app/services/shared-data.service';

@Component({
  selector: 'app-engagement',
  templateUrl: './engagement.page.html',
  styleUrls: ['./engagement.page.scss'],
})
export class EngagementPage implements OnInit {

  matchId:string;
  engagement:Engagement;
  constructor(private activateRoute:ActivatedRoute,private sharedDateSvc:SharedDataService) {

   }

  ngOnInit() {
    
    this.matchId = this.activateRoute.snapshot.paramMap.get('matchId');
    this.engagement = this.sharedDateSvc.getStudentLatestEngagmentByMatchId(this.matchId);
  }


}
