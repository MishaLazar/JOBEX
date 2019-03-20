import { Component } from '@angular/core';

/**
 * Generated class for the PersonalDataComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'personal-data',
  templateUrl: 'personal-data.html'
})
export class PersonalDataComponent {

  text: string;

  constructor() {
    console.log('Hello PersonalDataComponent Component');
    this.text = 'Hello World';
  }

}
