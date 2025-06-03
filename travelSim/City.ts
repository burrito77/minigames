import { Connection } from "./Connection";

export class City{

    // 0 - 1, decides range
    size:number = 0;
    name:string = "";
    position:number[] = [0,0]

    constructor(size:number,name:string,pos:number[]) {
        this.size = size;
        this.name = name;
        this.position = pos;
    }

    connectedCities:City[] = [];
    connections:Connection[] = [];
}