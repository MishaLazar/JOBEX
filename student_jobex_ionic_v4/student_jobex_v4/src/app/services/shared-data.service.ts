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

  
  skills:any;
  isSkillsLoaded:boolean = false;
  latestEngagements:Engagement[] = [];
  activeEngagements:Engagement[] = [];
  constructor(private http: HttpHelpService) { 
  
    this.skills = skillsJson;
    this.initStudentEngagements();
  }

  initStudentEngagements(){
    this.latestEngagements.push(new Engagement('ads22331','DBA','Keep close to Nature\'s heart... and break clear away, once in awhile,and climb a mountain or spend a week in the woods. Wash your spirit clean.',
    'NetApp','Bla Bla Bla', (5 * 0.8),'bla bla message'));
    this.latestEngagements.push(new Engagement('abdd2222','C#','Keep close to Nature\'s heart... and break clear away, once in awhile,and climb a mountain or spend a week in the woods. Wash your spirit clean.',
    'CyberArk','Bla Bla Bla', (5 * 0.9),'blaa balala message 2'));

    //TODO: delete prototype
    this.activeEngagements = this.latestEngagements.slice();
  }
  
  getStudentActiveEngagements(){
    return this.activeEngagements.slice();
  }

  getStudentLatestEngagments(){
    return this.latestEngagements.slice();
  }
  getStudentLatestEngagmentByMatchId(matchId:string){
    return this.latestEngagements.find(value => value.matchId == matchId);
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
