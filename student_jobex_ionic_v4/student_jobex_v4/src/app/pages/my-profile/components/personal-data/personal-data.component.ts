import {Component, Input, OnInit} from '@angular/core';
import {ModalController} from "@ionic/angular";
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { MyProfileService } from 'src/app/services/my-profile.service';

@Component({
  selector: 'app-personal-data',
  templateUrl: './personal-data.component.html',
  styleUrls: ['./personal-data.component.scss'],
})
export class PersonalDataComponent implements OnInit {

    personalData: FormGroup;
    profileImg: string = "assets/img/default_profile.png";
    text: string;
    @Input() value: any;
    constructor(
        private myProfile:MyProfileService, 
        private modalCtrl:ModalController,
        public formBuilder: FormBuilder
        ) {
       
        this.formBuild();
    }

    ngOnInit(): void {
        
            this.profileImg = this.myProfile.getMyProfileImgPath() ==undefined ? this.profileImg: this.myProfile.getMyProfileImgPath();
        
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
                    this.myProfile.getMyProfile()[control]= element.value;
                }
            }            
            this.myProfile.editProfileSave();
            this.modalCtrl.dismiss();
        }
        
    }
}
