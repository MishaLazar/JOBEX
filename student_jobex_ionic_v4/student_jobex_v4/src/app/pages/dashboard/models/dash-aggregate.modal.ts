class DateModal{
    constructor(public day:number,public month:number,public year:number){}
}

export class DashMatchesAggregateCount{

    constructor(
        public _id:DateModal,
        public count:number
    ){

    }
}

export class DashEngagementsAggregateCount{
    
    constructor(
        public _id:DateModal,
        public count:number
    ){

    }
}

export class DashMainChartCounts{

    constructor(){}
}