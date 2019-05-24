import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { ModalController, LoadingController } from '@ionic/angular';
import { Registration } from 'src/app/models/registration';

@Component({
    selector: 'app-personal-data',
    templateUrl: './personal-data.page.html',
    styleUrls: ['./personal-data.page.scss'],
})
export class PersonalDataPage implements OnInit {

    personalData: FormGroup;
    profileImg: string = "assets/img/default_profile.png";
    text: string;
    tempProfile: Registration;

    constructor(
        private profile: MyProfileService,
        private modalCtrl: ModalController,
        public formBuilder: FormBuilder,
        public loadingController:LoadingController
    ) {

        this.formBuild();
    }

    ngOnInit(): void {

        this.profileImg = this.profile.getMyProfileImgPath() == undefined ? this.profileImg : this.profile.getMyProfileImgPath();

    }

    loadPersonalData() {
        let studentData = this.profile.myProfile
    }
    formBuild() {
        this.personalData = this.formBuilder.group({
            firstName: [this.profile.myProfile.firstName ? this.profile.myProfile.firstName: '' , Validators.required],
            lastName: [this.profile.myProfile.lastName ? this.profile.myProfile.lastName: '', Validators.required],
            mail: [this.profile.myProfile.email ? this.profile.myProfile.email: '', Validators.compose([Validators.required, Validators.email])],
            phone: [this.profile.myProfile.phone ? this.profile.myProfile.phone: '', Validators.required],
            birthday: [this.profile.myProfile.birthday ? this.profile.myProfile.birthday: ''],
            address: [this.profile.myProfile.address ? this.profile.myProfile.address: '']

        })
    }

    async onPersonalDataUpdate(){
        if(!this.personalData.valid){
            console.log('registration form not valid');
        }    
        let basicProfile = new Registration(
          this.personalData.get('firstName').value,
          this.personalData.get('lastName').value,
          this.personalData.get('mail').value,
          null,
          null,null,false,this.personalData.get('address').value,null,null,this.personalData.get('phone').value,this.personalData.get('birthday').value);
    
        this.tempProfile = basicProfile;
        //this.myProfile.setMyProfileRegistration(basicProfile);
        
        let data = {
            student_id:this.profile.user_id,
            Profile:basicProfile
        }

        const loading = await this.loadingController.create({
          message:'login in ...'
        });
        loading.present();
        this.profile.onProfileDataUpdate(data).subscribe(
          (response:any) => {
              this.updateLocalProfileData();        
              loading.dismiss();
          },
          error => {
            console.log(error);
            loading.dismiss();
          }
        );
      }
    updateLocalProfileData() {
        this.profile.myProfile.firstName = this.tempProfile.firstName;
        this.profile.myProfile.lastName = this.tempProfile.lastName;
        this.profile.myProfile.email = this.tempProfile.email;
        this.profile.myProfile.address = this.tempProfile.address;
        this.profile.myProfile.phone = this.tempProfile.phone;
        this.profile.myProfile.birthday = this.tempProfile.birthday;

    }
}
