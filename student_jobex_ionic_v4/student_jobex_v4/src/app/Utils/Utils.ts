import { Count } from '../models/charts_models/counts.model';
import { connectableObservableDescriptor } from 'rxjs/internal/observable/ConnectableObservable';


export class Utils {


  static calculateAvgDataSet(DataSetToFill: number[], weeks: number, MatchesCounts: number[],EngagmentsCounts: number[]): any {
    let sum = 0;
    
    if(MatchesCounts.length == weeks){
        for (let index = 0; index < weeks; index++) {
            sum += MatchesCounts[index];        
        }
        DataSetToFill[0] = sum;
        DataSetToFill[0] = DataSetToFill[0] / (weeks)
        
    }

    sum = 0;
    if(EngagmentsCounts.length == weeks){
        for (let index = 0; index < weeks; index++) {
            sum += EngagmentsCounts[index];        
        }
        DataSetToFill[1] = sum;
        DataSetToFill[1] = DataSetToFill[1] / (weeks)
        
    }
    return DataSetToFill;
    
  }

    public static fillDataSetCounters(DataSet: number[], activation_date:Date, counts: Count[]): number[] {        
        counts.forEach(count => {
            let date = Date.parse(count._id.year + '/' + count._id.month + '/' + count._id.day);
            let week = Utils.weekesFromActivation(activation_date,date);
            DataSet[week-1] = DataSet[week-1] + count.count;
        })

        return DataSet;
    }

    // public static calculateAvgDataSet(DataSet: number[], activation_date:Date, counts: Count[]): number[]{
    //     let totalWeeks = Utils.weekesFromActivation(activation_date) - 1; //do not calc last week
    //     let sum = 0;
    //     for (let index = 0; index < totalWeeks; index++) {
    //         const element = array[index];
            
    //     }
    //     return DataSet;
    // }


    public static weekesFromActivation(activation_date, up_to_date?): number {
        if(!up_to_date){
            up_to_date = Date.now();
        }
        
        return Math.round((up_to_date - Date.parse(activation_date)) / (7 * 24 * 60 * 60 * 1000)) + 1;
    }
}