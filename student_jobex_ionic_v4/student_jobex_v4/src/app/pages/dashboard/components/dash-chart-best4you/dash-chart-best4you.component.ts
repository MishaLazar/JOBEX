import { Component, OnInit } from '@angular/core';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { PositionData } from 'src/app/models/position-data';
import { LoadingController } from '@ionic/angular';

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


  constructor(private profile:MyProfileService,private loadingController:LoadingController) { 
    
  }

  ngOnInit() {
    this.studentWishList = this.profile.wish_list.slice();
    
  }

  async loadWishListSuggestedSkill() {
    
    const loading = await this.loadingController.create({
      message: "loading.."
    });
    loading.present();
    this.profile.calculateWishlistSggestedSkill().then(
      (status:string) =>{
        if(status === 'success'){         
          console.log("success");
        }else{
          console.log("error loading studend skills");
        }
        loading.dismiss()        
      }
    );


    

  }

}
