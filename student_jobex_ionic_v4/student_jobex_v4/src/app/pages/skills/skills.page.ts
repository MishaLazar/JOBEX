import { Component, OnInit } from '@angular/core';
import { Skill } from 'src/app/models/skill.model';
import { ModalController, LoadingController, ToastController } from '@ionic/angular';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { MyProfileService } from 'src/app/services/my-profile.service';

@Component({
  selector: 'app-skills',
  templateUrl: './skills.page.html',
  styleUrls: ['./skills.page.scss'],
})
export class SkillsPage implements OnInit {

  skills:Skill[];
  SkillSearchTerm:any;
  constructor(
    public modalController: ModalController,
    private sharedData:SharedDataService,
    public myProfileService:MyProfileService, 
    public loadingController: LoadingController,
    public toastController: ToastController) {
    
    
  }

  ngOnInit() {
    this.loadSkills();
  }

  onSaveSkillsClick(){    
    this.myProfileService.onProfileSkillsUpdate();    
  }

  termChange(term:any){
    
    this.SkillSearchTerm = term.srcElement.value;
  }

  skillTuched(tuchedSkill:Skill){

    if(!tuchedSkill.IsChecked){
      this.myProfileService.removeSkillFromProfile(tuchedSkill);
    }
    else {
      this.myProfileService.addSkillToProfile(tuchedSkill);
    }

  }

  onLoadProfileSkills(){
    
    let profileSkills = this.myProfileService.getMyProfileSkills();
    let indexArray:number[] = [];
    profileSkills.forEach(profileSkill => {
      let index = this.skills.findIndex(el=> el.SkillId === profileSkill.SkillId);
      if(index >= 0){
        indexArray.push(index);
      }
    });

    if(indexArray.length > 0){
      indexArray.forEach(element => {
        this.skills[element].IsChecked = true;
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
            console.log(this.skills);
          }else {
            const toast = this.toastController.create({
              message: "Oops try again please",
              duration: 2000
            });
            
          }
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
