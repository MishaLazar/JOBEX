import {Component, OnInit} from '@angular/core';
import {MyProfileService} from "../../services/my-profile.service";
import {Form} from "ionic-angular";
import {collectExternalReferences} from "@angular/compiler";

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

  constructor(private profileService:MyProfileService ) {
    console.log('Hello PersonalDataComponent Component');
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

}
