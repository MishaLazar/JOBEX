import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'dash-engagments',
  templateUrl: './dash-engagments.component.html',
  styleUrls: ['./dash-engagments.component.scss'],
})
export class DashEngagmentsComponent implements OnInit {

  @Input() jobTitle:any;
  @Input() jobShortDescription:any;
  @Input() companyName:any;
  @Input() companyRating:any;
  constructor() {

    console.log(this.jobTitle);
   }

  ngOnInit() {}

}
