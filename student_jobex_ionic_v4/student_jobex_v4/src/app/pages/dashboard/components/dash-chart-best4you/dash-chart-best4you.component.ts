import { Component, OnInit } from '@angular/core';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { PositionData } from 'src/app/models/position-data';

@Component({
  selector: 'dash-chart-best4you',
  templateUrl: './dash-chart-best4you.component.html',
  styleUrls: ['./dash-chart-best4you.component.scss'],
})
export class DashChartBest4youComponent implements OnInit {

  studentWishList:PositionData[] = []
  CATEGORY = 0.1
  SUB_CATEGORY = 0.2
  SKILLS = 0.2
  OTHERS = 0.1
  LOCATION = 0.4


  constructor(private profile:MyProfileService) { 
    
  }

  ngOnInit() {
    this.studentWishList = this.profile.wish_list.slice();
    
  }

  calculateWhatIsBestForStudent(){

  }

}
