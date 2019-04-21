import { Component, OnInit } from '@angular/core';
import { ModalController } from '@ionic/angular';

@Component({
  selector: 'app-engagements',
  templateUrl: './engagements.component.html',
  styleUrls: ['./engagements.component.scss'],
})
export class EngagementsComponent implements OnInit {

  constructor(public modalController: ModalController ) { }

  ngOnInit() {}


  onClick(){
    this.modalController.dismiss();
  }
}
