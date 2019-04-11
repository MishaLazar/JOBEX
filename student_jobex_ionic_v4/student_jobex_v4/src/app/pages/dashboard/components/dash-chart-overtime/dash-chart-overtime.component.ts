import { Component, OnInit } from '@angular/core';
import Chart from 'chart.js';
@Component({
  selector: 'dash-chart-overtime',
  templateUrl: './dash-chart-overtime.component.html',
  styleUrls: ['./dash-chart-overtime.component.scss'],
})
export class DashChartOvertimeComponent implements OnInit {

  constructor() { }

  ngOnInit() {

    this.initOverTimeChart(['Matches', 'Engaged'],[20, 10],[15, 5]);
  }
  initOverTimeChart(chartLabels:string[],AvgDataSet:number[],CurrentDataSet:number[]): any {
    var ctx = (<any>document.getElementById('overTimeChart')).getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: chartLabels,
          
          datasets: [{ 
              label:"AVG.Weak",             
              data: AvgDataSet,
              backgroundColor: "#caf270",
              borderWidth: 1
          },
          { 
            label:"Weak4",             
            data: CurrentDataSet,
            backgroundColor: "#45c490",
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
                  ctx.fillText(data, bar._model.x, bar._model.y - 5);
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
