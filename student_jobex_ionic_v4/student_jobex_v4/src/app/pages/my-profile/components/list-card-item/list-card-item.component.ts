import {Component, Input, OnInit} from '@angular/core';

@Component({
    selector: 'list-card-item',
    templateUrl: './list-card-item.component.html',
    styleUrls: ['./list-card-item.component.scss'],
})
export class ListCardItemComponent implements OnInit {

    @Input() leftIconName: any;
    @Input() rightIconName: any;
    @Input() CardContentText: any;

    constructor() {
        console.log('Hello ListItemCardComponent Component is generated with params' + this.leftIconName + ',' + this.rightIconName + ',' + this.CardContentText);

    }

    ngOnInit() {
    }

}
