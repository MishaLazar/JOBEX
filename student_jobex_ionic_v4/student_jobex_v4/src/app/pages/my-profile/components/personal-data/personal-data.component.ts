import {Component, Input, OnInit} from '@angular/core';
import {MyProfileService} from "../../../../services/my-profile.service";
import {ModalController} from "@ionic/angular";
import { FormBuilder, Validators, FormGroup } from '@angular/forms';

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
        private profileService:MyProfileService, 
        private modalCtrl:ModalController,
        public formBuilder: FormBuilder
        ) {
        console.log('Hello PersonalDataComponent Component : ' + this.value);
        this.text = 'Hello World';
        this.formBuild();
    }

    ngOnInit(): void {
        if(this.profileService.isProfileImgSet()){
            this.profileImg = this.profileService.myProfile.profileImg;
        }
    }

    onSubmit(form:any){
      console.log(form);

      this.CloseModal();
    }

    private CloseModal() {
        this.modalCtrl.dismiss();
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
        console.log(this.personalData.valid)
        console.log(this.personalData.value)
    }
}
