import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import skillsJson from '../testDataFiles/skills.json';
@Injectable({
  providedIn: 'root'
})
export class SharedDataService {


  skills:any;
  constructor(private httpClient: HttpClient) { 
    // this.getSkillJson().subscribe(data => {
    //     this.skills = data;
    //     console.log(this.skills);
    // });
    //console.log(skillsJson);
    this.skills = skillsJson;
  }
  
}
