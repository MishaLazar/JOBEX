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
       

    }

    ngOnInit() {
    }

}
