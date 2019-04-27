import { Component, OnInit } from '@angular/core';
import Chart from 'chart.js';
import { matches } from '@ionic/core/dist/types/components/nav/view-controller';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { Utils } from 'src/app/Utils/Utils';
@Component({
  selector: 'dash-chart-active-engagements',
  templateUrl: './dash-chart-active-engagements.component.html',
  styleUrls: ['./dash-chart-active-engagements.component.scss'],
})
export class DashChartActiveEngagementsComponent implements OnInit {

  constructor(private profile:MyProfileService) { }

  ngOnInit() {
    let weeks:number = Utils.weekesFromActivation(this.profile.myProfile.activation_data);
    let MatchesDataSet = new Array(weeks).fill(0);
    let ActiveEngagementsDataSet = new Array(weeks).fill(0);
    ActiveEngagementsDataSet = Utils.fillDataSetCounters(ActiveEngagementsDataSet,this.profile.myProfile.activation_data,this.profile.engagemtnsCounts);
    
    MatchesDataSet = Utils.fillDataSetCounters(MatchesDataSet,this.profile.myProfile.activation_data,this.profile.matchesCounts);
    
    this.initActiveEngagementsDonat(weeks,MatchesDataSet,ActiveEngagementsDataSet);
  }

  initActiveEngagementsDonat(weeks:number,MatchesDataSet:number[],ActiveEngagementsDataSet:number[]): any {
    let chartLabels:string[] = [];
    for (let index = 0; index < weeks; index++) {
      const label = 'week' + (index+1);
      chartLabels.push(label);   
    }
    var ctx = (<any>document.getElementById('activeEngagementsChart')).getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: chartLabels,
          
          datasets: [{ 
              label:"Chart Overtime",             
              data: MatchesDataSet,
              fill: false,
              backgroundColor: [
                  'rgba(0,255,0,0.3)'
                  
              ],
              borderWidth: 1
          },
          { 
            label:"Chart Overtime",             
            data: ActiveEngagementsDataSet,
            backgroundColor: [
                
                'rgba(255, 99, 132, 0.2)'
                
            ],
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
