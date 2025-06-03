import { City } from "./City"
import { Connection } from "./Connection"
import { cities } from "./Generator"

export class Player{
    position:number[] = []
    city:City = cities[0]
    money:number = 100

    inCity:boolean = true
    inMotion:boolean = false

    currentConnection:Connection|undefined = undefined
    
    sitOnConnection(conn:Connection){
        this.currentConnection = conn;
    }
}