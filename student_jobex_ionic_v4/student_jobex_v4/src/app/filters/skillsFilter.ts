import { PipeTransform, Pipe, OnInit } from '@angular/core';
import { Skill } from '../models/skill.model';
import { MyProfileService } from '../services/my-profile.service';

@Pipe({
    name: 'SkillFilter'
  })
  export class SkillFilterPipe implements PipeTransform {
  

    
    constructor(){
      
    }

  
    
    transform(value: Skill[], skill: string) {
      var skillStatmentToSearch = skill;     
      if (skill !== undefined && skill.length >= 2) {
        skill = skill.toLowerCase();        
        return value.filter(function(el: any) {                            
          return el["TextValue"].toLowerCase().indexOf(skillStatmentToSearch) > -1;
        });
      }
      return [];
    }
  }