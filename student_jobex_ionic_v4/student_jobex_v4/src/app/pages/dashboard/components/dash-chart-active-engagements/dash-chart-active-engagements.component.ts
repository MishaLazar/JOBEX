import { Component, OnInit } from '@angular/core';
import Chart from 'chart.js';
import { matches } from '@ionic/core/dist/types/components/nav/view-controller';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { Utils } from 'src/app/Utils/Utils';
import { Subscription } from 'rxjs';

@Component({
  selector: 'dash-chart-active-engagements',
  templateUrl: './dash-chart-active-engagements.component.html',
  styleUrls: ['./dash-chart-active-engagements.component.scss'],
})
export class DashChartActiveEngagementsComponent implements OnInit {

  pLoadedSubject:Subscription;
  activeChartReady:boolean = false;
  constructor(private profile:MyProfileService) { }

  ngOnInit() {
    
    if(!this.profile.myProfile){
      this.pLoadedSubject = this.profile.profileLoadedSubject.subscribe(
        (value) =>{
          if(value == 'loaded'){
            this.loadActiveEngagmentChart();
            this.pLoadedSubject.unsubscribe();
          }
        }
      );
      this.profile.loadProfile();  
    }else{
      this.loadActiveEngagmentChart();
    }
    
  }
  onViewWillUnload(){
    if(this.pLoadedSubject){
      this.pLoadedSubject.unsubscribe();
    }
  }
  loadActiveEngagmentChart(){
    
    if(!this.profile.engagemtnsCounts || !this.profile.matchesCounts){
      this.profile.chartCounterSubject.subscribe(
        (value) => {
          if(value =='loaded'){
            this.populateData();
          }
      });
      this.profile.loadChartCounters();
    }
    else{
      this.populateData();
    }

  }

  populateData(){
    let weeks:number = Utils.weekesFromActivation(this.profile.myProfile.activation_date);
    let MatchesDataSet = new Array(weeks).fill(0);
    let ActiveEngagementsDataSet = new Array(weeks).fill(0);
    ActiveEngagementsDataSet = Utils.fillDataSetCounters(ActiveEngagementsDataSet,this.profile.myProfile.activation_date,this.profile.engagemtnsCounts);
    MatchesDataSet = Utils.fillDataSetCounters(MatchesDataSet,this.profile.myProfile.activation_date,this.profile.matchesCounts);
    this.activeChartReady = true;
    this.initActiveEngagements(weeks,MatchesDataSet,ActiveEngagementsDataSet);
    
    
  }

  initActiveEngagements(weeks:number,MatchesDataSet:number[],ActiveEngagementsDataSet:number[]): any {
    let chartLabels:string[] = [];
    for (let index = 0; index < weeks; index++) {
      const label = 'week' + (index+1);
      chartLabels.push(label);   
    }
    let activeEngagementsPlaceholder =(<any>document.getElementById('activeEngagementsPlaceHolder'));
    activeEngagementsPlaceholder.setAttribute("class","background");
    var ctx = (<any>document.getElementById('activeEngagementsChart')).getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: chartLabels,
          
          datasets: [{ 
              label:"Chart Overtime",             
              data: MatchesDataSet,
              fill: false,
              backgroundColor: "#004D7F",
              borderWidth: 1
          },
          { 
            label:"Chart Overtime",             
            data: ActiveEngagementsDataSet,
            backgroundColor: "#0095DA",
            borderWidth: 1
        }]
      },
      options: {
        circumference: Math.PI,
        rotation : Math.PI,
        cutoutPercentage : 80,
          maintainAspectRatio: false,
          plugins: {
					  datalabels: {
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
						  borderColor: '#ffffff',
              color: function(context) {
							  return context.dataset.backgroundColor;
						  },

            
              
            }
        },
          legend: {
            "display": false
          },
          tooltips: {
            "enabled": false
          },
          scales: {
            xAxes: [{
                gridLines: {
                  color: "rgba(0, 0, 0, 0)",
              }
            }],
            yAxes: [{
                ticks:{
                  display:false,
                  beginAtZero: true,                  
                  max:Math.max.apply(Math,MatchesDataSet) + 3
                },                
                // gridLines: {
                //     color: "rgba(0, 0, 0, 0)",
                //     offsetGridLines: false
                // }
            }]
          },
      //     scales: {
      //       xAxes: [{
      //           gridLines: {
      //             color: "rgba(0, 0, 0, 0)",
      //         }
      //       }],
      //       yAxes: [{
      //           ticks:{
      //             display:false,
      //             beginAtZero: true,                  
      //             max:Math.max.apply(Math,chartData) + 3
      //           },                
      //           gridLines: {
      //               color: "rgba(0, 0, 0, 0)",
      //               offsetGridLines: false
      //           }
      //       }]
      //     },
          animation: {
         
        	duration: 1,
						onComplete: function () {
							var chartInstance = this.chart,
              ctx = chartInstance.ctx;
							
							ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
							ctx.textAlign = 'center';
							ctx.textBaseline = 'bottom';
              
							this.data.datasets.forEach(function (dataset, i) {
								var meta = chartInstance.controller.getDatasetMeta(i);
								meta.data.forEach(function (bar, index) {
									var data = dataset.data[index];                            
									ctx.fillText(data, bar._model.x, bar._model.y - 5);
								});
							});
						}
        },
      }          
  });
  }
}
