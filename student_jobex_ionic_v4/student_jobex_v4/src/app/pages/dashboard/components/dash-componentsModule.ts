import { NgModule } from '@angular/core';
import { DashEngagmentsComponent } from './dash-engagments/dash-engagments.component';
import { DashChartActiveEngagementsComponent } from './dash-chart-active-engagements/dash-chart-active-engagements.component';
import { DashChartBest4youComponent } from './dash-chart-best4you/dash-chart-best4you.component';
import { DashChartOvertimeComponent } from './dash-chart-overtime/dash-chart-overtime.component';

@NgModule({
    declarations:[DashEngagmentsComponent,DashChartActiveEngagementsComponent,DashChartBest4youComponent,DashChartOvertimeComponent],
    imports:[],
    exports:[DashEngagmentsComponent,DashChartActiveEngagementsComponent,DashChartBest4youComponent,DashChartOvertimeComponent],
    entryComponents:[]
})
export class DashComponentsModul{}