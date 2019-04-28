import { SkillList } from './student_skill';

export class PositionData{
    constructor(
        public position_name:string,
        public position_department:string,
        public position_skill_list:SkillList[]
    ){
        

    }
    
}