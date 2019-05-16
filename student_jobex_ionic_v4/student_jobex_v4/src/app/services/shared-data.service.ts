import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import skillsJson from '../testDataFiles/skills.json';
import { Engagement } from '../models/engagement.js';
import { HttpHelpService } from './http-help.service.js';
import { Skill } from '../models/skill.model.js';
import { PositionData } from '../models/position-data.js';
@Injectable({
  providedIn: 'root'
})
export class SharedDataService {

  
  skills:Skill[];  
  latestEngagements:Engagement[] = [];
  activeEngagements:Engagement[] = [];
  positionsDataset:PositionData[];
  skillsLoadedSubject:Subject<string> = new Subject();
  positionDataSetLoadedSubject:Subject<string> = new Subject();

  constructor(private http: HttpHelpService) { 
  
    //this.skills = skillsJson;    
    this.initStudentEngagements();
    this.loadPositionDataset();
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
      if(!this.skills){
        this.http.get('resources/skills').subscribe(
          (data:Skill[]) => {
            this.skills = data;
            this.skillsLoadedSubject.next('loaded');
            console.log('loaded :' + data.length + ' skills');
          },
          error =>{
            console.log(error);
          }
  
        );
      }
  }

  loadPositionDataset(){
    
      this.http.get('resources/getPositionDataSet').subscribe(
        (data:PositionData[]) => {          
          this.positionsDataset = data;          
          this.positionDataSetLoadedSubject.next('loaded');
          console.log('loaded :' + data.length + ' positionsDataset');
        },
        error =>{
          console.log(error);
        }

      );
    }
  
   getSkillTextValueById(skill_id) {
     if(!this.skills){
       return "Oops!";
     }
     let skill_result = this.skills.find(skill => skill.SkillId == skill_id )
     return skill_result.TextValue;
   }
}
