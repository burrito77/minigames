import { City } from "./City";

export class Connection{

    constructor(startStation:City,endStation:City,passingStation:City[],type:ConnectionType,departureTime:number) {
        this.startStation=startStation;
        this.endStation=endStation;
        this.passingStations=passingStation;
        this.type=type;
        this.departureTime=departureTime;
    }

    startStation:City;
    endStation:City;
    passingStations:City[]
    type:ConnectionType
    departureTime:number

}

export enum ConnectionType{
    os,
    sp,
    r,
    ex,
    ic,
    ADMIN,
}

