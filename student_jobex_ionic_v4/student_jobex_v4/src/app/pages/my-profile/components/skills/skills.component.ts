import { Component, OnInit } from '@angular/core';
import { ModalController } from '@ionic/angular';

@Component({
  selector: 'app-skills',
  templateUrl: './skills.component.html',
  styleUrls: ['./skills.component.scss'],
})
export class SkillsComponent implements OnInit {

  constructor(public modalController: ModalController) { }

  ngOnInit() {}

  onClick(){
    this.modalController.dismiss();
  }

}
