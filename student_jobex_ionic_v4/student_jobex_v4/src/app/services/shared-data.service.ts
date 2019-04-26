import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import skillsJson from '../testDataFiles/skills.json';
import { Engagement } from '../models/engagement.js';
import { HttpHelpService } from './http-help.service.js';
import { Skill } from '../models/skill.model.js';
@Injectable({
  providedIn: 'root'
})
export class SharedDataService {

  
  skills:Skill[];
  isSkillsLoaded:boolean = false;
  latestEngagements:Engagement[] = [];
  activeEngagements:Engagement[] = [];
  constructor(private http: HttpHelpService) { 
  
    this.skills = skillsJson;
    this.initStudentEngagements();
  }

  initStudentEngagements(){
    //TODO: delete prototype
    this.activeEngagements = this.latestEngagements.slice();
  }
  
  getStudentActiveEngagements(){
    return this.activeEngagements.slice();
  }

  getStudentLatestEngagments(){
    return this.latestEngagements.slice();
  }
  getStudentLatestEngagmentByMatchId(match_Id:string){
    return this.latestEngagements.find(value => value.match_id == match_Id);
  }
  loadAllSkills(){
    if(!this.isSkillsLoaded){
      this.http.get('resources/skills').subscribe(
        (data:Skill[]) => {
          this.skills = data;
          this.isSkillsLoaded = true;
          //console.log('loaded :' + data.length + ' skills');
        },
        error =>{
          console.log(error);
        }

      );
    }
  }
}
