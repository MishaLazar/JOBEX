import { Component, OnInit } from '@angular/core';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { Engagement } from 'src/app/models/engagement';
import { NavController } from '@ionic/angular';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { HttpHelpService } from 'src/app/services/http-help.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {


  studentLastEgagements: Engagement[];
  mayChartDisplay: boolean = false;
  constructor(
    private sharedDataSvc: SharedDataService,
    private http: HttpHelpService,
    private navCtrl: NavController, 
    private profile: MyProfileService) { }

  ngOnInit() {    
    this.profile.loadProfile();
    this.loadDashCharts();
    this.studentLastEgagements = this.sharedDataSvc.getStudentLatestEngagments();
    this.sharedDataSvc.loadAllSkills();
  }

  loadDashCharts() {
    
    if(!this.profile.engagemtnsCounts|| !this.profile.matchesCounts){
      this.profile.profileLoadedSubject.subscribe(
        (value) => {
          if (value == 'loaded') {
            let data = {
              user_id: this.profile.user_id
            }
            this.http.submitForm(data, 'get_dashboard_main_chart_data').subscribe(
              (data: any) => {
                this.mayChartDisplay = true;
                this.profile.engagemtnsCounts = data["engagements_counts"];
                this.profile.matchesCounts =  data["matches_couts"];
            
              },
              (error) => {
                console.log(error);
              }
            )
          }
        });
      }
      else{
        this.mayChartDisplay = true;
      }
  }

  // onClickTest(mid:string){
  //   this.navCtrl.navigateForward('dashboard/engagement/'+mid);
  // }
  onClick() {
    this.profile.loadStudentSkills();
  }
}
