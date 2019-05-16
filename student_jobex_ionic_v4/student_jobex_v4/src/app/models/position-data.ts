import { SkillList } from './student_skill';

export class PositionData{
    constructor(
        public position_name:string,
        public position_department:string,
        
        public IsChecked:boolean = false,
        public position_skill_list:SkillList[],
        public position_location_id:number = -1,
        public position_location_description:string = ""
    ){
        

    }
    
}