import { PipeTransform, Pipe, } from '@angular/core';
import { PositionData } from '../models/position-data';
@Pipe({
    name: 'PositionTitleFilter'
})
export class PositionTitleFilterPipe implements PipeTransform {
    constructor() {

    }
    transform(value: PositionData[], title: string) {               
        if (title !== undefined && title.length >= 2) {            
            title = title.toLowerCase();
            return value.filter(function (el: any) {
                return el["position_name"].toLowerCase().indexOf(title) > -1;
            });
        }
        return [];
    }
}