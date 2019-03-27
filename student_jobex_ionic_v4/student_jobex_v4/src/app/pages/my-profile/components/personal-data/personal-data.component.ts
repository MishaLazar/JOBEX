import {Component, Input, OnInit} from '@angular/core';
import {MyProfileService} from "../../../../services/my-profile.service";
import {ModalController} from "@ionic/angular";

@Component({
  selector: 'app-personal-data',
  templateUrl: './personal-data.component.html',
  styleUrls: ['./personal-data.component.scss'],
})
export class PersonalDataComponent implements OnInit {

    profileImg: string = "assets/img/default_profile.png";
    text: string;
    @Input() value: any;
    constructor(private profileService:MyProfileService, private modalCtrl:ModalController) {
        console.log('Hello PersonalDataComponent Component : ' + this.value);
        this.text = 'Hello World';

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
}
