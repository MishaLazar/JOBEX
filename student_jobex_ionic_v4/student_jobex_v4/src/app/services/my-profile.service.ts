import { Injectable, OnDestroy } from '@angular/core';
import { MyProfile } from "../models/my-profile.model";
import { Skill } from '../models/skill.model';
import { HttpHelpService } from './http-help.service';
import { SkillList } from '../models/student_skill';
import { LiteSkill } from '../models/lite.skill.modal';

import { ConfigService } from './config.service';
import { Observable, Subject } from 'rxjs';

import { Registration } from '../models/registration';
import { Count } from '../models/charts_models/counts.model';
import { PositionData } from '../models/position-data';
import { Engagement } from '../models/engagement';
import { NavController } from '@ionic/angular';

@Injectable({
    providedIn: 'root'
})
export class MyProfileService  {
    
    
    // ngOnDestroy(): void {
    //     this.isFirstLogin = true;
    //     console.log("MyProfileService destroy");

    // }

    isFirstLogin:boolean = true;
    myProfile: MyProfile;
    user_id: string;
    isProfileLoaded: boolean = false;
    isUpdated: boolean = false;
    myStudentSkills: SkillList[] = [];
    myProfileSkills: Skill[] = [];
    wish_list: PositionData[] = [];
    isActiveProfile: boolean;
    profileLoadedSubject: Subject<string> = new Subject();
    WL_SuggestedSubject: Subject<string> = new Subject();
    OverTimeChartSubject: Subject<string> = new Subject();
    ActiveEngagmentSubject: Subject<string> = new Subject();
    chartCounterSubject: Subject<string> = new Subject();
    
    wl_suggested: any;
    latestEngagemants: Engagement[];

    //chartsData
    matchesCounts: Count[];
    engagemtnsCounts: Count[];

    constructor(private http: HttpHelpService, private config: ConfigService,public navCtrl:NavController) {

    }    
    clearProfileData(){
        this.myProfile = undefined;
        // this.myProfileSkills = [];
        // this.myStudentSkills = [];
        // this.engagemtnsCounts = undefined;
        // this.matchesCounts = undefined;
        // this.wish_list = [];
        // this.wl_suggested = undefined;
        // this.latestEngagemants = undefined;

    }
    loadProfile() {
        if (!this.myProfile) {
            const data = {
                user_id: this.user_id
            }
            this.http.submitForm(data, 'get_student_profile').subscribe(
                (data: MyProfile) => {
                    
                    this.myProfile = data;
                    this.myStudentSkills = this.myProfile.student_skill_list;
                    this.wish_list = this.myProfile.wish_list;
                    this.processLoadedStudentSkill();
                    //this.calculateWishlistSggestedSkill();
                    this.profileLoadedSubject.next('loaded');
                },
                (error: any) => {
                    this.navCtrl.navigateRoot('/login')
                }
            );
        }

    }


    setMyProfileRegistration(myProfile: MyProfile) {
        this.myProfile = myProfile;
        this.isUpdated = true;
    }

    processLoadedStudentSkill() {
        
        this.myStudentSkills.forEach(sSkill => {
            sSkill.skills.forEach(skill => {
                let s = new Skill(skill.skill_Id, null, sSkill.sub_category_id, sSkill.category_id, true);
                if(this.myProfileSkills.findIndex(mskill => mskill.SkillId === s.SkillId) < 0){
                    this.myProfileSkills.push(s)
                }
                
            });
        });
    }


    getMyProfileSkills() {
        return this.myProfileSkills.slice();
    }

    addSkillToProfile(skillToAdd: Skill) {
        
        let foundStudentSkill = this.myStudentSkills.findIndex(skill => skill.category_id === skillToAdd.SkillCategoryId && skill.sub_category_id === skillToAdd.SkillSubCategoryId)
        if (foundStudentSkill >= 0) {
            this.myStudentSkills[foundStudentSkill].skills.push(new LiteSkill(skillToAdd.SkillId));
        }
        else {
            let newSkill = new SkillList(skillToAdd.SkillCategoryId, skillToAdd.SkillSubCategoryId);
            newSkill.skills.push(new LiteSkill(skillToAdd.SkillId));
            this.myStudentSkills.push(newSkill);
        }
        this.myProfileSkills.push(skillToAdd);
    }
    removeSkillFromProfile(skillToRemove: Skill) {
        let foundStudentSkill = this.myStudentSkills.findIndex(skill => skill.category_id === skillToRemove.SkillCategoryId && skill.sub_category_id === skillToRemove.SkillSubCategoryId)
        if (foundStudentSkill >= 0) {
            let skillIndex = this.myStudentSkills[foundStudentSkill].skills.findIndex(skill => skill.skill_Id === skillToRemove.SkillId);
            if (skillIndex >= 0) {
                this.myStudentSkills[foundStudentSkill].skills.splice(skillIndex, 1);
                if (this.myStudentSkills[foundStudentSkill].skills.length == 0) {
                    this.myStudentSkills.splice(foundStudentSkill, 1);
                }
            }

        }
        var indexToRemove = this.myProfileSkills.findIndex(el => el.SkillId == skillToRemove.SkillId);
        if (indexToRemove >= 0) {
            this.myProfileSkills.splice(indexToRemove, 1);
        }
    }

    onRegistration(basicProfile: Registration) {

        return this.http.submitForm(basicProfile, 'student/register');

    }

    onProfileDataUpdate(updatedProfile: any) {

        return this.http.submitForm(updatedProfile, 'student/update_profile');

    }

    onProfileSkillsUpdate() {
        return this.http.submitForm(this.myStudentSkills.slice(), 'student/update_skills/' + this.user_id).subscribe(
            (response) => {
                //console.log(response);
            },
            (error: any) => {
                console.log(error);
            }

        )
    }
    setUserIdOnLogin(user_id: string) {
        //this.clearProfileData();
        this.user_id = user_id;
    }

    onUpdateProfileActivation() {
        let data = {
            user_id: this.user_id,
            active_status: this.isActiveProfile
        }
        this.http.submitForm(data, 'activate_student_profile').subscribe(
            (response: any) => {

                //console.log(response);
            },
            error => {
                console.log(error);
            }
        );
    }

    getMyProfileImgPath() {
        return this.myProfile.profileImg
    }

    getMyProfile() {
        return this.myProfile;
    }

    loadLatestsEngagements(maxOfLatests: number): Observable<Object> {
        let data = {
            student_id: this.user_id,
            limit: this.config.getMaxNumOfLatests()
        }
        return this.http.submitForm(data, 'student/getStudentEngagements');
    }
    getStudentEngagments(): Observable<Object> {
        return this.http.get('student/getStudentEngagements/' + this.user_id);
    }

    calculateWishlistSggestedSkill() {
        const data = {
            student_id: this.user_id,
            student_skills: this.myStudentSkills,
            wl_positions: this.wish_list
        }
        this.http.submitForm(data, 'student/wish_list/calculate_suggested_skill').subscribe(
            (data: any) => {   
                          
                const wl_suggested_result = {
                    diff: data['diff'],
                    new_match_level_id: data['new_match_level_id'],
                    old_match_level_id: data['old_match_level_id'],
                    new_skill_category_id: data['new_skill'][0],
                    new_skill_sub_category_id: data['new_skill'][1],
                    new_skill_skill_id: data['new_skill'][2]
                }
                this.wl_suggested = wl_suggested_result;
                console.log(this.wl_suggested);
                this.WL_SuggestedSubject.next('success');

            },
            (error) => {
                console.log(error);
                this.WL_SuggestedSubject.next('failed');
            }
        )

    }
    loadChartCounters() {

        if (!this.engagemtnsCounts || !this.matchesCounts) {
            let data = {
                user_id: this.user_id
            }
            this.http.submitForm(data, 'get_dashboard_main_chart_data').subscribe(
                (data: any) => {                    
                    this.engagemtnsCounts = data["engagements_counts"];
                    this.matchesCounts = data["matches_couts"];
                    this.chartCounterSubject.next('loaded');
                },
                (error) => {
                    console.log(error);
                    this.chartCounterSubject.next('failed');
                }
            );
        }


    }

    // calculateWishlistSggestedSkill(){
    //     return new Promise((resolve,reject) =>{

    //         let data = {
    //             student_id: this.user_id,
    //             student_skills:this.myStudentSkills,
    //             wl_positions:this.wish_list
    //         }
    //         this.http.submitForm(data,'student/wish_list/calculate_suggested_skill').toPromise()
    //         .then(
    //             (data:any) => { 

    //                 const wl_suggested_result = {
    //                     diff:data['diff'],
    //                     new_match_level_id:data['new_match_level_id'],
    //                     old_match_level_id:data['old_match_level_id'],
    //                     new_skill_category_id:data['new_skill'][0],
    //                     new_skill_sub_category_id:data['new_skill'][1],
    //                     new_skill_skill_id:data['new_skill'][2]
    //                 }
    //                 this.wl_suggested = wl_suggested_result;
    //                 console.log(this.wl_suggested);
    //                 this.WL_SuggestedSubject.next('success');

    //             },
    //             (error) =>{
    //                 console.log(error);
    //                 this.WL_SuggestedSubject.next('failed');
    //             }
    //         )
    //     });
    // }

    getLatestEngagemants(): Engagement[] {
        return this.latestEngagemants.slice();
    }
    setLatestEngagemants(engagements: Engagement[]) {
        this.latestEngagemants = engagements;
    }


}
