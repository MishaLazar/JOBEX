import {Component, Input} from '@angular/core';

/**
 * Generated class for the ListItemCardComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'list-item-card',
  templateUrl: 'list-item-card.html'
})
export class ListItemCardComponent {


  @Input() leftIconName: any;
  @Input() rightIconName: any;
  @Input() CardContentText: any;

  constructor() {
    console.log('Hello ListItemCardComponent Component is generated with params' + this.leftIconName  + ',' + this.rightIconName + ',' + this.CardContentText);

  }

}
