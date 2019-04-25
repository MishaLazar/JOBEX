import { Component, OnInit } from '@angular/core';
import { Engagement } from 'src/app/models/engagement';
import { NavController, LoadingController } from '@ionic/angular';
import { MyProfileService } from 'src/app/services/my-profile.service';

@Component({
  selector: 'app-engagements-list',
  templateUrl: './engagements-list.page.html',
  styleUrls: ['./engagements-list.page.scss'],
})
export class EngagementsListPage implements OnInit {

  Engagements:Engagement[];
  constructor(private profile:MyProfileService,private navCtrl:NavController,private  loadingController: LoadingController) { }

  ngOnInit() {
    this.onLoadEngagments();
  }
  
  openEngagment(match_id:string){
    this.navCtrl.navigateForward('my-profile/engagements-list/engagement/' + match_id);
  }

  async onLoadEngagments(){
    const loading = await this.loadingController.create({
      message : 'loading ...'
    });
    loading.present();
    this.profile.getStudentEngagments().subscribe(
      (data:Engagement[]) =>{
        this.Engagements = data;
        console.log(this.Engagements)
        loading.dismiss();
      },
      (error) => {
        console.log(error)
        loading.dismiss();
      }
    );
  }

}
