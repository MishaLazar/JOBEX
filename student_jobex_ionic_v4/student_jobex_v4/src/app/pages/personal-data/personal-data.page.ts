import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { ModalController } from '@ionic/angular';

@Component({
  selector: 'app-personal-data',
  templateUrl: './personal-data.page.html',
  styleUrls: ['./personal-data.page.scss'],
})
export class PersonalDataPage implements OnInit {

  personalData: FormGroup;
  profileImg: string = "assets/img/default_profile.png";
  text: string;
  
  constructor(
      private myProfile:MyProfileService, 
      private modalCtrl:ModalController,
      public formBuilder: FormBuilder
      ) {
     
      this.formBuild();
  }

  ngOnInit(): void {
      if(this.myProfile.isProfileImgSet()){
          this.profileImg = this.myProfile.myProfile.profileImg;
      }
  }


  private formBuild(){
      this.personalData = this.formBuilder.group({
          firsName:['',Validators.required],
          lastName:['',Validators.required],
          mail:['',Validators.compose([Validators.required,Validators.email])],
          phone:[''],
          birthday:[''],
          address:['']
          
      })
  }

  onProfileSave(){
      if(!this.personalData.valid){

      }else{
          for (const control in this.personalData.controls) {
              if (this.personalData.controls.hasOwnProperty(control)) {
                  const element = this.personalData.controls[control];
                  this.myProfile.myProfile[control] = element.value;
              }
          }            
          this.myProfile.editProfileSave();
          this.modalCtrl.dismiss();
      }
      
  }

}
