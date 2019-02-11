import {MyProfile} from "../models/my-profile.model";

export class MyProfileService {

  myProfile

  constructor(){
    this.myProfile =  new MyProfile(
      "Misha","lazar","misha.lazar89@gmail.com","Object1","address city","assets/imgs/tests/deadpool-profile.png"
    )
  }

  editProfileSave(profile:MyProfile){
    if (profile != null){
      this.myProfile = profile;
    }
  }

  loadProfile(){
    return this.myProfile;
  }

  isProfileImgSet(){
    return this.myProfile.profileImg != null && this.myProfile.profileImg.length > 0 ? true:false;
  }

}
