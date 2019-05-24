import { SkillList } from './student_skill';
import { PositionData } from './position-data';

export class MyProfile{

  constructor(public firstName:string,
              public lastName:string,
              public email:string,              
              public userId:string,
              public address:string,
              public location:number,
              public active:boolean,
              public profileImg:string,
              public creation_data:Date,
              public activation_data:Date,
              public student_skill_list:SkillList[],
              public wish_list:PositionData[],
              public phone:string = "",
              public birthday:Date = null
              ){}

}
