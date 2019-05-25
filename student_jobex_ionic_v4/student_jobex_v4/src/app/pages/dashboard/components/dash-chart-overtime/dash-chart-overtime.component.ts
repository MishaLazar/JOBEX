import { Component, OnInit } from '@angular/core';
import Chart from 'chart.js';
import { Utils } from 'src/app/Utils/Utils';
import { MyProfileService } from 'src/app/services/my-profile.service';
@Component({
  selector: 'dash-chart-overtime',
  templateUrl: './dash-chart-overtime.component.html',
  styleUrls: ['./dash-chart-overtime.component.scss'],
})
export class DashChartOvertimeComponent implements OnInit {

  constructor(public profile:MyProfileService) { }

  ngOnInit() { 
    let weeks:number = Utils.weekesFromActivation(this.profile.myProfile.activation_date);
    let MatchesDataSet = new Array(weeks).fill(0);
    let ActiveEngagementsDataSet = new Array(weeks).fill(0);
    let AvgMatchesDataSet = new Array(2).fill(0);
    let CurrentWeekDataSet = new Array(2).fill(0);
    ActiveEngagementsDataSet = Utils.fillDataSetCounters(ActiveEngagementsDataSet,this.profile.myProfile.activation_date,this.profile.engagemtnsCounts);    
    MatchesDataSet = Utils.fillDataSetCounters(MatchesDataSet,this.profile.myProfile.activation_date,this.profile.matchesCounts);
    AvgMatchesDataSet = Utils.calculateAvgDataSet(AvgMatchesDataSet,weeks,MatchesDataSet,ActiveEngagementsDataSet);
    CurrentWeekDataSet[0] = MatchesDataSet[weeks-1];
    CurrentWeekDataSet[1] = ActiveEngagementsDataSet[weeks-1];    
    this.initOverTimeChart(['Matches', 'Engaged'],AvgMatchesDataSet,CurrentWeekDataSet);
  }
  initOverTimeChart(chartLabels:string[],AvgDataSet:number[],CurrentDataSet:number[]): any {
    var ctx = (<any>document.getElementById('overTimeChart')).getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: chartLabels,
          
          datasets: [{ 
              label:"AVG.Week",             
              data: AvgDataSet,
              backgroundColor: "#004D7F",
              borderWidth: 1
          },
          { 
            label:"Current Week",             
            data: CurrentDataSet,
            backgroundColor: "#0095DA",
            borderWidth: 1
        }
        ]
      },
      options:{
        tooltips: {
          displayColors: true,
          callbacks:{
            mode: 'x',
          },
        },
        scales: {
          xAxes: [{
            stacked: true,
            gridLines: {
              display: false,
            }
          }],
          yAxes: [{
            stacked: true,
            display:false,
            ticks: {
              max: AvgDataSet[0] + CurrentDataSet[0] + 3,
              display:false,
              beginAtZero: true,
            },
            gridLines:{
              display: false,
            },
            type: 'linear',
          }]
        },
        responsive: true,
        maintainAspectRatio: false,
        legend: { position: 'bottom' },
        animation: {
          duration: 1,
            onComplete: function () {
              var chartInstance = this.chart,
                ctx = chartInstance.ctx;
              
              ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
              ctx.textAlign = 'center';
              ctx.textBaseline = 'middle'
              

              this.data.datasets.forEach(function (dataset, i) {
                var meta = chartInstance.controller.getDatasetMeta(i);
                meta.data.forEach(function (bar, index) {
                 
                  var data = dataset.data[index]; 
                  if(data > 0){
                    ctx.fillText(data, bar._model.x, bar._model.y - 5);
                  }                           
                  
                });
              });
            }
        }
       
      }
  //     options: {
  //         maintainAspectRatio: false,
  //         legend: {
  //           "display": true
  //         },
  //         tooltips: {
  //           "enabled": false
  //         },
  //         scales: {
  //           //stacked: true,
  //           xAxes: [{
  //               gridLines: {
  //                 color: "rgba(0, 0, 0, 0)",
  //             }
  //           }],
  //           yAxes: [{
  //             stacked: true,
  //               ticks:{
  //                 display:false,
  //                 beginAtZero: true,                  
  //                 //max:Math.max.apply(Math,chartData) + 3
  //               },                
  //               gridLines: {
  //                   color: "rgba(0, 0, 0, 0)",
  //                   offsetGridLines: false
  //               }
  //           }]
  //         },
  //        ,
  //     }          
  });
  }

}
