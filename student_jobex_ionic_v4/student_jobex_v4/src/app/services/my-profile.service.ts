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
    private user_id:string;
    isProfileLoaded:boolean = false;
    isUpdated:boolean = false;
    myProfileSkills:Skill[]=[
        new Skill('a',44,'MySql',1,1,true),
        new Skill('b',108,'PL/SQL',1,2,true)
    ];
    isActiveProfile: boolean;


    constructor(private http:HttpHelpService){
        
    }

    editProfileSave(){
        
    }

    loadProfile(){
        const data = {
            user_id:this.user_id
        }
        if(!this.isProfileLoaded){
            this.http.submitForm(data,'get_student_profile').subscribe(
                (data:MyProfile) =>{
                    this.myProfile = data;
                    this.isProfileLoaded = true;
                },
                (error:any) =>{
                    console.log(error);
                }
            );
        }
        
    }
    setMyProfileRegistration(myProfile:MyProfile){
        this.myProfile = myProfile;
        this.isUpdated = true;
    }

    // isProfileImgSet(){
    //     return this.myProfile.profileImg != null && this.myProfile.profileImg.length > 0 ? true:false;
    // }

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
    setUserIdOnLogin(user_id:string){
        this.user_id = user_id;
    }

    onUpdateProfileActivation(){
        let data = {
            user_id:this.user_id,
            active_status:this.isActiveProfile
        }
        this.http.submitForm(data,'activate_student_profile').subscribe(
            (response:any) =>{
                debugger;
                console.log(response);
            },
            error => {
                console.log(error);
            }
        );
    }

    getMyProfileImgPath(){
        return this.myProfile.profileImg
    }

    getMyProfile(){
        return this.myProfile;
    }
}
