import { Injectable } from '@angular/core';
import {MyProfile} from "../models/my-profile.model";
import { Skill } from '../models/skill.model';

@Injectable({
  providedIn: 'root'
})
export class MyProfileService {

    myProfile;
    myProfileSkills:Skill[]=[
        new Skill('a',44,'MySql',1,1,true),
        new Skill('b',108,'PL/SQL',1,2,true)
    ];
    constructor(){
        this.myProfile =  new MyProfile(
            "Misha","lazar","misha.lazar89@gmail.com","Object1","address city","/assets/img/deadpool-profile.png"
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

    getMyProfileSkills(){
        return this.myProfileSkills.slice();
    }

    addSkillToProfile(skillToAdd:Skill){
        this.myProfileSkills.push(skillToAdd);
    }
    removeSkillFromProfile(skillToRemove:Skill){
        var indexToRemove = this.myProfileSkills.findIndex(el => el.SkillId == skillToRemove.SkillId);
        if(indexToRemove > 0){
            this.myProfileSkills.splice(indexToRemove,1);
        }
    }
       
    
}
