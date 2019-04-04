import { Component, OnInit } from '@angular/core';
import { ModalController } from '@ionic/angular';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { Skill } from 'src/app/models/skill.model';

@Component({
  selector: 'app-skills',
  templateUrl: './skills.component.html',
  styleUrls: ['./skills.component.scss'],
})
export class SkillsComponent implements OnInit {

  skills:Skill[];
  SkillSearchTerm:any;
  constructor(public modalController: ModalController,private sharedData:SharedDataService) {
    this.skills = this.sharedData.skills.slice();
    
   }

  ngOnInit() {

  }

  onClick(){
    this.modalController.dismiss();
  }

  termChange(term:any){
    
    this.SkillSearchTerm = term.srcElement.value;
  }
  
}
