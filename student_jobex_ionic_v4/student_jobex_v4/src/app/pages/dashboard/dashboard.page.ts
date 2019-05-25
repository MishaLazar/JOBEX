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
  overTimeChartReady:boolean = false;
  
  mayChartDisplay: boolean = false;
  constructor(
    private sharedDataSvc: SharedDataService,
    private http: HttpHelpService,
    private navCtrl: NavController, 
    private profile: MyProfileService) { }

  ngOnInit() {    
    // this.profile.loadProfile();
    // this.studentLastEgagements = this.sharedDataSvc.getStudentLatestEngagments();
    // this.loadDashCharts();
    // this.sharedDataSvc.loadAllSkills();
    // this.sharedDataSvc.loadAllCities();
  }

  ionViewWillEnter(){
  

    if(!this.profile.myProfile){
      this.profile.profileLoadedSubject.subscribe((value) =>{
        if (value == 'loaded'){
          this.studentLastEgagements = this.sharedDataSvc.getStudentLatestEngagments();
          this.loadDashCharts();
          this.sharedDataSvc.loadAllSkills();
          this.sharedDataSvc.loadAllCities();
        }else{
          console.log('Dashboard, Oops cant load profile');
        }
      });
      this.profile.loadProfile();
    }
    else {
      this.studentLastEgagements = this.sharedDataSvc.getStudentLatestEngagments();
      this.loadDashCharts();
      this.sharedDataSvc.loadAllSkills();
      this.sharedDataSvc.loadAllCities();
    }
    
  }
  loadDashCharts() {
    
    if(!this.profile.engagemtnsCounts || !this.profile.matchesCounts){
      
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
  
}
