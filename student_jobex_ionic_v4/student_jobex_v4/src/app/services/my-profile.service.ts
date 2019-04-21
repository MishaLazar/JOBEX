import { Injectable } from '@angular/core';
import {MyProfile} from "../models/my-profile.model";
import { Skill } from '../models/skill.model';
import { HttpHelpService } from './http-help.service';
import { error } from 'protractor';

@Injectable({
  providedIn: 'root'
})
export class MyProfileService {

    myProfile:MyProfile;
    user_id:string;
    isUpdated:boolean = false;
    myProfileSkills:Skill[]=[
        new Skill('a',44,'MySql',1,1,true),
        new Skill('b',108,'PL/SQL',1,2,true)
    ];
    constructor(private http:HttpHelpService){
        this.myProfile =  new MyProfile(
            "Misha","lazar","misha.lazar89@gmail.com","Object1","address city","/assets/img/deadpool-profile.png"
        )
    }

    editProfileSave(){
        
    }

    loadProfile(){
        this.http.submitForm('','get_student_profile').subscribe(
            (data:MyProfile) =>{
                this.myProfile = data;
            },
            (error:any) =>{
                console.log(error);
            }
        );
    }
    setMyProfileRegistration(myProfile:MyProfile){
        this.myProfile = myProfile;
        this.isUpdated = true;
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
    
    onRegistration(basicProfile:MyProfile){

       return this.http.submitForm(basicProfile,'register_student');

    }
    
    onProfileSkillsUpdate(){           
        return this.http.submitForm(this.myProfileSkills.slice(),'student/update_skills/'+this.myProfile.userId).subscribe(() => 
        (error:any) => {
            console.log(error);
        },
        (response) => {
            console.log(response);
        }
        )
    }

}
