import { PipeTransform, Pipe } from '@angular/core';
import { Skill } from '../models/skill.model';

@Pipe({
    name: 'SkillFilter'
  })
  export class SkillFilterPipe implements PipeTransform {
    transform(value: Skill[], skill: string):Skill[] {
        debugger;
      if (skill !== undefined && skill.length >= 2) {
        skill = skill.toLowerCase();        
        return value.filter(function(el: any) {
          return el["TextValue"].toLowerCase().indexOf(skill) > -1;
        });
      }
      return [];
    }
  }