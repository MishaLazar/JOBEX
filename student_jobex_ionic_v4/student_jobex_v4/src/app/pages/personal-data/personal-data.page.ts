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
        private profile: MyProfileService,
        private modalCtrl: ModalController,
        public formBuilder: FormBuilder
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
            firsName: [this.profile.myProfile.firstName, Validators.required],
            lastName: [this.profile.myProfile.lastName, Validators.required],
            mail: [this.profile.myProfile.email, Validators.compose([Validators.required, Validators.email])],
            phone: [this.profile.myProfile.phone],
            birthday: [this.profile.myProfile.birthday],
            address: [this.profile.myProfile.address]

        })
    }

    onProfileSave() {
        if (!this.personalData.valid) {

        } else {
            for (const control in this.personalData.controls) {
                if (this.personalData.controls.hasOwnProperty(control)) {
                    const element = this.personalData.controls[control];
                    this.profile.getMyProfile()[control] = element.value;
                }
            }
            this.profile.editProfileSave();
            this.modalCtrl.dismiss();
        }

    }

}
