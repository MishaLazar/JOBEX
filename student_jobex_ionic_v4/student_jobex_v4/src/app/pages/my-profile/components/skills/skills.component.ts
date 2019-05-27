import { Component, OnInit } from '@angular/core';
import { ModalController } from '@ionic/angular';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { Skill } from 'src/app/models/skill.model';
import { MyProfileService } from 'src/app/services/my-profile.service';

@Component({
  selector: 'app-skills',
  templateUrl: './skills.component.html',
  styleUrls: ['./skills.component.scss'],
})
export class SkillsComponent implements OnInit {

  skills:Skill[];
  SkillSearchTerm:any;
  constructor(public modalController: ModalController,private sharedData:SharedDataService,public myProfileService:MyProfileService) {
    this.skills = this.sharedData.skills.slice();
    
  }

  ngOnInit() {
    this.init();
  }

  onSaveSkillsClick(){
   
    this.myProfileService.onProfileSkillsUpdate();
    this.modalController.dismiss();
  }

  termChange(term:any){
    
    this.SkillSearchTerm = term.srcElement.value;
  }

  skillTuched(tuchedSkill:Skill){

    if(tuchedSkill.IsChecked){
      this.myProfileService.removeSkillFromProfile(tuchedSkill);
    }
    else {
      this.myProfileService.addSkillToProfile(tuchedSkill);
    }

  }

  init(){
    
    let profileSkills = this.myProfileService.getMyProfileSkills();
    let indexArray:number[] = [];
    profileSkills.forEach(profileSkill => {
      let index = this.skills.findIndex(el=> el.SkillId === profileSkill.SkillId);
      if(index > 0){
        indexArray.push(index);
      }
    });

    if(indexArray.length > 0){
      indexArray.forEach(element => {
        this.skills[element].IsChecked = true;
      });
    }
  }
  
}
