import { Component, OnInit } from '@angular/core';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { Engagement } from 'src/app/models/engagement';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {


  studentLastEgagements:Engagement[];
  constructor(private sharedDataSvc:SharedDataService) { }

  ngOnInit() {
    this.studentLastEgagements = this.sharedDataSvc.getStudentEngagments();
    console.log(this.studentLastEgagements);
  }



}
