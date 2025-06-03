import { City } from "./City";
import { Connection, ConnectionType } from "./Connection";
import { Player } from "./Player";

export let cities:City[] = []
export let player:Player;
export function generateCities(mapsize:number,citiesNumber:number,development:number = 0.93){
    for(let i = 0; i < citiesNumber; i++){

        // 1 - evenly distributed, <1 - more villages, >1 - more cities
        let random = Math.random();
        let size = Math.min(development * random, 1);
        size = parseFloat(size.toFixed(1));


        let first:string[] = ["mi","pl","na","do","ho","če","ba","a","vy","zl","ne","ku","sre","le","ta","za","pa","dno"];
        let second:string [] = ["ku","no","bi","re","mni","rov","no","hu","í","gr","bo","ta","za","ha","ko","vy","ur","tru","cho"];
        let third:string[] = ["ovice","ov","lupy","ta","lice","vice","í","a","o","u","vy","ha","en","ven","kot","ot","py","dek","va","ouc"];

        random = Math.round(Math.random() * (first.length-1))
        let name = first[random]
        random = Math.round(Math.random() * (second.length-1))
        name = name + second[random]
        random = Math.round(Math.random() * (third.length-1))
        name = name + third[random]

        let posx = Math.round(Math.random() * mapsize)
        let posy = Math.round(Math.random() * mapsize)

        cities.push(new City(size,name,[posx,posy]))
    }
}

export function generateConnectingCities(distanceMultiplier:number = 1,init_val:number = 300){
       for(let i = 0;i<cities.length;i++){
            for(let j=0;j<cities.length;j++){
                if(j<=i){
                    continue;
                }else{
                    let dis = getDistance(cities[i],cities[j])
                    if(dis <= distanceMultiplier*init_val*Math.max(cities[i].size,cities[j].size)){
                        cities[i].connectedCities.push(cities[j]);
                        cities[j].connectedCities.push(cities[i]);
                    }
                }
            }
       }
}

export function generateConnections(numberOfConnectionsAtMaxSize:number = 500){
    cities.forEach((startCity)=>{
        startCity.connectedCities.forEach((endCity)=>{
           let avgsize = (startCity.size + endCity.size)/2
           let numberOfConnections = Math.round(numberOfConnectionsAtMaxSize * avgsize * avgsize * avgsize * avgsize + (Math.random() - 0.5)*20)
           for(let i = 0;i<numberOfConnections;i++){

               startCity.connections.push(new Connection(startCity,endCity,[],getRandomConnectionType(),Math.floor(Math.random() * (24*60+1))))
           }
        })
    })
}

export function generatePlayer(){
    player = new Player()
    player.city = cities[0];
}

export function printCities(){
    cities.forEach((city)=>{
        console.log(`City: ${city.name} POS: [${city.position[0]},${city.position[1]}] size: ${city.size} connectedCities: ${city.connectedCities.length}`)
    })
}

export function printConnectedCities(){
    cities.forEach((city)=>{
        city.connectedCities.forEach(ccity=>{
            console.log(`${city.name} - ${ccity.name} DISTANCE: ${getDistance(ccity,city)}`);
        })
    })
}

export function printConnections(){
    cities.forEach(city=>{
        city.connections.forEach(conn=>{
            console.log(`${conn.startStation.name} -> ${conn.endStation.name} | ${ConnectionType[conn.type]} ||| ${conn.departureTime}`)
        })
    })
}


export function getDistance(city1:City,city2:City):number{
     const [x1, y1] = city1.position;
     const [x2, y2] = city2.position;

    const dx = x2 - x1;
    const dy = y2 - y1;

    return Math.sqrt(dx * dx + dy * dy);
}

function getRandomConnectionType(): ConnectionType {
    const rand = Math.random();

    if (rand < 0.5) return ConnectionType.os;       // 50%
    else if (rand < 0.7) return ConnectionType.sp;  // 20%
    else if (rand < 0.85) return ConnectionType.r;  // 15%
    else if (rand < 0.95) return ConnectionType.ex; // 10%
    else return ConnectionType.ic;                  // 5%
}