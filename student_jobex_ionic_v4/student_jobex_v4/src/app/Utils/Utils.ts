import { Count } from '../models/charts_models/counts.model';
import { connectableObservableDescriptor } from 'rxjs/internal/observable/ConnectableObservable';


export class Utils {

    public static fillDataSetCounters(DataSet: number[], activation_date:Date, counts: Count[]): number[] {        
        counts.forEach(count => {
            let date = Date.parse(count._id.year + '/' + count._id.month + '/' + count._id.day);
            let week = Utils.weekesFromActivation(activation_date,date);
            DataSet[week-1] = DataSet[week-1] + count.count;
        })

        return DataSet;
    }

    public static weekesFromActivation(activation_date, up_to_date?): number {
        if(!up_to_date){
            up_to_date = Date.now();
        }

        return Math.round((up_to_date - Date.parse(activation_date)) / (7 * 24 * 60 * 60 * 1000));
    }
}