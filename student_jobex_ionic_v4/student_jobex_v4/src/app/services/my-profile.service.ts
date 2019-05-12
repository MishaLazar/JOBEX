import { Injectable } from '@angular/core';
import {MyProfile} from "../models/my-profile.model";
import { Skill } from '../models/skill.model';
import { HttpHelpService } from './http-help.service';
import { SkillList } from '../models/student_skill';
import { LiteSkill } from '../models/lite.skill.modal';
import { switchMap, catchError } from 'rxjs/operators';
import { ConfigService } from './config.service';
import { Observable, Subject } from 'rxjs';
import { Engagement } from '../models/engagement';
import { Registration } from '../models/registration';
import { Count} from '../models/charts_models/counts.model';
import { PositionData } from '../models/position-data';

@Injectable({
  providedIn: 'root'
})
export class MyProfileService {
 
 

    myProfile:MyProfile;
    user_id:string;
    isProfileLoaded:boolean = false;
    isUpdated:boolean = false;
    myStudentSkills:SkillList[] = [];
    myProfileSkills:Skill[]=[];
    wish_list:PositionData[] = [];
    isActiveProfile: boolean;
    isStudentSkillsLoaded: boolean = false;
    profileLoadedSubject:Subject<string> = new Subject();


    //chartsData
    matchesCounts:Count[];
    engagemtnsCounts:Count[];

    constructor(private http:HttpHelpService,private config:ConfigService){
        
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
                    this.myStudentSkills = this.myProfile.student_skill_list;
                    this.loadStudentSkills();
                    this.loadWishlist();
                    this.isProfileLoaded = true;
                    this.profileLoadedSubject.next('loaded');
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

    loadStudentSkills(){        
        if(!this.isStudentSkillsLoaded){
            // this.http.get('student/skills/' + this.user_id).subscribe(
            //     (skills:SkillList[]) =>{
        
            this.isStudentSkillsLoaded = true;                
            this.processLoadedStudentSkill(this.myStudentSkills);
                // },
                // (error:any) =>{
                //     console.log(error);
                // });            
        }
    }
    processLoadedStudentSkill(studentSkills: SkillList[]) {
        studentSkills.forEach(sSkill => {
            sSkill.skills.forEach(skill => {
                this.myProfileSkills.push(new Skill(skill.skill_Id,null,sSkill.sub_category_id,sSkill.category_id,true))
            });
        });
    }
    // isProfileImgSet(){
    //     return this.myProfile.profileImg != null && this.myProfile.profileImg.length > 0 ? true:false;
    // }

    getMyProfileSkills(){
        return this.myProfileSkills.slice();
    }

    addSkillToProfile(skillToAdd:Skill){
        let foundStudentSkill = this.myStudentSkills.findIndex(skill => skill.category_id === skillToAdd.SkillCategoryId && skill.sub_category_id === skillToAdd.SkillSubCategoryId)
        if(foundStudentSkill >= 0){
            this.myStudentSkills[foundStudentSkill].skills.push(new LiteSkill(skillToAdd.SkillId));
        }
        else {
            let newSkill = new SkillList(skillToAdd.SkillCategoryId,skillToAdd.SkillSubCategoryId);
            newSkill.skills.push(new LiteSkill(skillToAdd.SkillId));
            this.myStudentSkills.push(newSkill);
        }
        this.myProfileSkills.push(skillToAdd);
    }
    removeSkillFromProfile(skillToRemove:Skill){
        let foundStudentSkill = this.myStudentSkills.findIndex(skill => skill.category_id === skillToRemove.SkillCategoryId && skill.sub_category_id === skillToRemove.SkillSubCategoryId)
        if(foundStudentSkill >= 0){
            let skillIndex = this.myStudentSkills[foundStudentSkill].skills.findIndex(skill => skill.skill_Id === skillToRemove.SkillId);
            if(skillIndex >= 0){
                this.myStudentSkills[foundStudentSkill].skills.splice(skillIndex,1);
                if(this.myStudentSkills[foundStudentSkill].skills.length == 0){
                    this.myStudentSkills.splice(foundStudentSkill,1);
                }
            }

        }
        var indexToRemove = this.myProfileSkills.findIndex(el => el.SkillId == skillToRemove.SkillId);
        if(indexToRemove >= 0){
            this.myProfileSkills.splice(indexToRemove,1);
        }
    }
    
    onRegistration(basicProfile:Registration){

       return this.http.submitForm(basicProfile,'register_student');

    }
    
    onProfileSkillsUpdate(){           
        return this.http.submitForm(this.myStudentSkills.slice(),'student/update_skills/'+this.user_id).subscribe(
            (response) => {
                debugger;
                this.isStudentSkillsLoaded = false;
                console.log(response);
            },
            (error:any) => {
            console.log(error);
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

    loadLatestsEngagements(maxOfLatests: number): Observable<Object> {
        let data = {
            student_id:this.user_id,
            limit:this.config.getMaxNumOfLatests()
        }
        return this.http.submitForm(data,'student/getStudentEngagements');
    }
    getStudentEngagments(): Observable<Object> {        
        return this.http.get('student/getStudentEngagements/'+this.user_id);
    }

    loadWishlist():Promise<string> {
        return new Promise((resolve, reject) => {
            let data = {
                student_id: this.user_id
            }
            this.http.submitForm(data,'student/get_wish_list').toPromise()
                .then(
                    (data:PositionData[]) =>{
                  
                        this.wish_list = data;
                        console.log(this.wish_list);
                        resolve("success");
                      }
                      ,
                    (error) => {
                    
                    console.log(error);
                    resolve("error");
                    
                    }
                )
                
                });
        } 
    
    
    calculateWishlistSggestedSkill():Promise<string>{
        return new Promise((resolve,reject) =>{

            let data = {
                student_id: this.user_id,
                student_skills:this.myStudentSkills,
                wl_positions:this.wish_list
            }
            this.http.submitForm(data,'student/wish_list/calculate_suggested_skill').toPromise()
            .then(
                (data:any) => {
                    debugger;
                    console.log(data);
                    resolve("success");
                },
                (error) =>{
                    console.log(error);
                    resolve("error");
                }
            )
        });
    }
}
