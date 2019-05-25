import { SkillList } from './student_skill';

export class Registration{

    constructor(public firstName:string,
                public lastName:string,
                public email:string,
                public username:string,
                public password:string,
                public userId:string,
                public active:boolean,
                public address:string,
                public profileImg:string,
                public student_skill_list:SkillList[],
                public phone:string = "",
                public birthday:Date = null,
                public location:number = -1,
                public user_type:string = "student"
                ){}
  
  }