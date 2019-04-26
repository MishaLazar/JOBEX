import { LiteSkill } from './lite.skill.modal';

export class SkillList{

    constructor(
        public category_id:number,
        public sub_category_id:number,
        public skills:LiteSkill[] = []
    ){}
}