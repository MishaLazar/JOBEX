import { Component, OnInit } from '@angular/core';
import { Skill } from 'src/app/models/skill.model';
import { ModalController, LoadingController, ToastController } from '@ionic/angular';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { HttpHelpService } from 'src/app/services/http-help.service';

@Component({
  selector: 'app-skills',
  templateUrl: './skills.page.html',
  styleUrls: ['./skills.page.scss'],
})
export class SkillsPage implements OnInit {

  skills:Skill[];
  profileSkills:Skill[];
  SkillSearchTerm:any;
  inSaveProcess:boolean =  false;
  constructor(
    public modalController: ModalController,
    private sharedData:SharedDataService,
    public profile:MyProfileService, 
    public loadingController: LoadingController,
    public toastController: ToastController,
    private http:HttpHelpService
    ) {
    
    
  }

  ngOnInit() {
    this.loadSkills();
  }

  onSaveSkillsClick(){  
    this.inSaveProcess = true;
    return this.http.submitForm(this.profile.myStudentSkills.slice(),'student/update_skills/'+this.profile.user_id).subscribe(
      (response) => {
        this.inSaveProcess = false;        
      },
      (error:any) => {
        console.log(error);
      }
  
  )
   
    
  }

  termChange(term:any){
    
    this.SkillSearchTerm = term.srcElement.value;
  }

  // skillTuched(tuchedSkill:Skill){

  //   if(!tuchedSkill.IsChecked){
  //     this.profile.removeSkillFromProfile(tuchedSkill);
  //   }
  //   else {
  //     this.profile.addSkillToProfile(tuchedSkill);
  //   }

  // }


  skillTuched(skill:Skill) {
    if (skill.IsChecked) {
      this.profileSkills.push(skill);
      let indexToRmove = this.skills.indexOf(skill);
      if (indexToRmove >= 0) {
        this.skills.splice(indexToRmove, 1)
        this.profile.addSkillToProfile(skill);
      }
    }
    else{
      this.skills.push(skill);
      let indexToRmove = this.profileSkills.indexOf(skill);
      if (indexToRmove >= 0) {
        this.profileSkills.splice(indexToRmove, 1)
        this.profile.removeSkillFromProfile(skill);
      }
    }
  }

  removeProfileSkills(skill:Skill) {
    skill.IsChecked = false;
    this.skills.push(skill);
    let indexToRmove = this.profileSkills.indexOf(skill);
    if (indexToRmove >= 0) {
      this.profileSkills.splice(indexToRmove, 1)
      this.profile.removeSkillFromProfile(skill);
    }
  }

  onLoadProfileSkills(){
   
    this.profileSkills = this.profile.getMyProfileSkills();    
    let indexArray:number[] = [];
    this.profileSkills.forEach(profileSkill => {
      let index = this.skills.findIndex(el=> el.SkillId === profileSkill.SkillId);
      if(index >= 0){
        indexArray.push(index);
        profileSkill.TextValue = this.skills[index].TextValue;
      }
    });

    if(indexArray.length > 0){
      indexArray.forEach(element => {
        //this.skills[element].IsChecked = true;
        this.skills.splice(element, 1)
      });
    }
  }

  async loadSkills(){
    
    if(!this.sharedData.skills){
      const loading = await this.loadingController.create({
          message:"loading.."
      });
      loading.present();
      this.sharedData.skillsLoadedSubject.subscribe(
        (value) =>{
          
          if(value == 'loaded'){
            
            this.finallizeLoading();            
          }else {
            const toast = this.toastController.create({
              message: "Oops try again please",
              duration: 2000
            });
            
          }
          this.sharedData.skillsLoadedSubject.unsubscribe();
          loading.dismiss()
        }        
      );
      this.sharedData.loadAllSkills();
    }
    else{
      this.finallizeLoading();
    }
  }

  finallizeLoading(){
    this.skills = this.sharedData.skills.slice();   
    this.onLoadProfileSkills();
  }
}
