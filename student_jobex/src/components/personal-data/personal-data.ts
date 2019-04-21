import {Component, Input, OnInit} from '@angular/core';
import {MyProfileService} from "../../services/my-profile.service";
import {ModalController, ViewController} from "ionic-angular";

/**
 * Generated class for the PersonalDataComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */


@Component({
  selector: 'personal-data',
  templateUrl: 'personal-data.html'
})

export class PersonalDataComponent implements OnInit{
  profileImg: string = "../assets/imgs/default_profile.png";
  text: string;
  @Input() value: number;
  constructor(private profileService:MyProfileService, private viewController:ViewController) {
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
  }

  dismiss() {
      this.viewController.dismiss();

  }

}
