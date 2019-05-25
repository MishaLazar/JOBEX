import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Engagement } from '../models/engagement.js';
import { HttpHelpService } from './http-help.service.js';
import { Skill } from '../models/skill.model.js';
import { PositionData } from '../models/position-data.js';
import { City } from '../models/City.js';
@Injectable({
  providedIn: 'root'
})
export class SharedDataService {

  
  skills:Skill[];  
  latestEngagements:Engagement[] = [];
  activeEngagements:Engagement[] = [];
  positionsDataset:PositionData[];
  skillsLoadedSubject:Subject<string> = new Subject();
  citiesLoadedSubject:Subject<string> = new Subject();
  positionDataSetLoadedSubject:Subject<string> = new Subject();
  cities: City[];

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
            
          },
          error =>{
            console.log(error);
          }
  
        );
      }else{
        this.skillsLoadedSubject.next('loaded');
      }
  }
  
  loadAllCities(){
    if(!this.cities){
      this.http.get('resources/cities').subscribe(
        (data:City[]) => {
          this.cities = data;
          this.citiesLoadedSubject.next('loaded');
          console.log('loaded :' + data.length + ' cities');
        },
        error =>{
          console.log(error);
        }

      );
    }else{
      this.citiesLoadedSubject.next('loaded');
    }
}
  loadPositionDataset(){
      if(!this.positionsDataset){
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
      }else {
        this.positionDataSetLoadedSubject.next('loaded');
      }
      
    }
  
   getSkillTextValueById(skill_id) {
     if(!this.skills){
       return "Oops!";
     }
     let skill_result = this.skills.find(skill => skill.SkillId == skill_id )
     return skill_result.TextValue;
   }

   getAllSkill(){
    
     if(this.skills){
        this.skillsLoadedSubject.next('loaded');        
     }else {
        
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
}
