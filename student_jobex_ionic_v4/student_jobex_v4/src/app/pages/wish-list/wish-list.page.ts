import { Component, OnInit } from '@angular/core';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { PositionData } from 'src/app/models/position-data';
import { LoadingController, ToastController } from '@ionic/angular';
import { HttpHelpService } from 'src/app/services/http-help.service';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { load } from '@angular/core/src/render3';

@Component({
  selector: 'app-wish-list',
  templateUrl: './wish-list.page.html',
  styleUrls: ['./wish-list.page.scss'],
})
export class WishListPage implements OnInit {

  positionDataset: PositionData[];
  positionSelected: PositionData[] = [];
  JobTitleSearchTerm: any
  inSaveProcess:boolean = false;
  constructor(
    private profile: MyProfileService,
    private sharedData: SharedDataService,
    public loadingController: LoadingController,
    public toastController: ToastController,
    private http: HttpHelpService) {


  }

  ngOnInit() {
    this.positionSelected = this.profile.wish_list.slice();        
    //this.loadPositionDataSet();

  }

  ionViewWillEnter(){
    this.loadPositionDataSet();
  }
  // async loadWishList() {
    
  //   const loading = await this.loadingController.create({
  //     message: "loading.."
  //   });
  //   loading.present();
  //   this.profile.loadWishlist().then(
  //     (status:string) =>{
  //       if(status === 'success'){
  //         this.positionSelected = this.profile.wish_list.slice();        
  //         this.loadPositionDataSet();
  //         console.log(this.positionSelected);
  //       }else{
  //         console.log("error loading studend skills");
  //       }
  //       loading.dismiss()        
  //     }
  //   );


    

  // }


  async loadPositionDataSet(){
    const loading = await this.loadingController.create({
          message: "loading.."
        });
    loading.present();
    if (!this.sharedData.positionsDataset) {
      
      this.sharedData.positionDataSetLoadedSubject.subscribe(
        (value) => {
          
          if (value == 'loaded') {
            this.positionDataset = this.sharedData.positionsDataset.slice();
            this.finallizeLoading();
            
          } else {
            const toast = this.toastController.create({
              message: "Oops try again please",
              duration: 2000
            });

          }
          loading.dismiss();
        }
      );
      this.sharedData.loadPositionDataset();
    }
    else {
      
      this.positionDataset = this.sharedData.positionsDataset.slice();
      this.finallizeLoading();
      loading.dismiss();
    }
  }

  finallizeLoading() {
    
    this.positionSelected.forEach(ps => {
      let index = this.positionDataset.findIndex(
        el => el.position_name === ps.position_name && ps.position_department === el.position_department);
      if(index >= 0){
        console.log(index);
        this.positionDataset.splice(index,1);
      }
    });
  }

  positionTuched(position: PositionData) {
    if (position.IsChecked) {
      this.positionSelected.push(position);
      let indexToRmove = this.positionDataset.indexOf(position);
      if (indexToRmove >= 0) {
        this.positionDataset.splice(indexToRmove, 1)
      }
    }
  }

  removeFromWishList(position: PositionData) {
    position.IsChecked = false;
    this.positionDataset.push(position);
    let indexToRmove = this.positionSelected.indexOf(position);
    if (indexToRmove >= 0) {
      this.positionSelected.splice(indexToRmove, 1)
    }
  }

  async onWishListSaveClick() {
    const loading = await this.loadingController.create({
      message:"Saving..."
    });
    loading.present();
    this.inSaveProcess = true;
    let data = {
      student_id: this.profile.user_id,
      wish_list: this.positionSelected
    }
    this.http.submitForm(data, 'student/wish_list_save').subscribe(
      (Response) => {
        loading.dismiss();
        //console.log(Response);
        this.inSaveProcess = false;
      },
      (error) => {
        loading.dismiss();
        console.log(error);
        this.inSaveProcess = false;
      }

    )
  }
}
