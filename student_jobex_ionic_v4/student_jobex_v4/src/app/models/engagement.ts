import { SkillList } from './student_skill';

export class Engagement{
    constructor(
        public _id:string,
        public position_id:string,
        public student_id:string,
        public match_id:string,
        public position_description:string,
        public position_title:string,
        public position_location:string,
        public company_name:string,        
        public message:string,
        public is_new:boolean,
        public status:string,
        public is_deleted:boolean,
        public match_level_id:number,
        public creation_date:Date,
        public position_skill_list:SkillList[]
        ){}
}