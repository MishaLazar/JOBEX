import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import skillsJson from '../testDataFiles/skills.json';
import { Engagement } from '../models/engagement.js';
@Injectable({
  providedIn: 'root'
})
export class SharedDataService {

  
  skills:any;
  engagements:Engagement[] = [];
  constructor(private httpClient: HttpClient) { 
    // this.getSkillJson().subscribe(data => {
    //     this.skills = data;
    //     console.log(this.skills);
    // });
    //console.log(skillsJson);
    this.skills = skillsJson;
    this.initStudentEngagements();
  }

  initStudentEngagements(){
    this.engagements.push(new Engagement('DBA','Keep close to Nature\'s heart... and break clear away, once in awhile,and climb a mountain or spend a week in the woods. Wash your spirit clean.',
    'NetApp','Bla Bla Bla', (5 * 0.8)));
    this.engagements.push(new Engagement('C#','Keep close to Nature\'s heart... and break clear away, once in awhile,and climb a mountain or spend a week in the woods. Wash your spirit clean.',
    'CyberArk','Bla Bla Bla', (5 * 0.9)));
  }
  
  getStudentEngagments(){
    return this.engagements.slice();
  }
}
