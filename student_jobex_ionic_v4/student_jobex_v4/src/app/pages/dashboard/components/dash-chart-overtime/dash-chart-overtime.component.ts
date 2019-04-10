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

    this.useAnotherOneWithWebpack(['Red', 'Blue'],[12, 19]);
  }
  useAnotherOneWithWebpack(chartLabels:string[],chartData:number[]): any {
    var ctx = (<any>document.getElementById('overTimeChart')).getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: chartLabels,
          
          datasets: [{ 
              label:"Chart Overtime",             
              data: chartData,
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)'
              ],
              borderWidth: 1
          }]
      },
      options: {
          maintainAspectRatio: false,
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
                  max:Math.max.apply(Math,chartData) + 3
                },                
                gridLines: {
                    color: "rgba(0, 0, 0, 0)",
                    offsetGridLines: false
                }
            }]
          },
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
