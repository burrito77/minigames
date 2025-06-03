import { ConnectionType } from "./Connection";
import { getDistance, player } from "./Generator";

const ConnectionSpeeds: Record<ConnectionType, number> = {
    [ConnectionType.os]: 60,
    [ConnectionType.sp]: 90,
    [ConnectionType.r]: 120,
    [ConnectionType.ex]: 160,
    [ConnectionType.ic]: 220,
    [ConnectionType.ADMIN]: 7777
};

let initialArrival = 0;

export async function awaitDeparture() {
    if (!player.currentConnection || player.inMotion) {
        return;
    }
    initialArrival = player.currentConnection.departureTime + getDistance(player.currentConnection.startStation,player.currentConnection.endStation)/ConnectionSpeeds[player.currentConnection.type] 
    const now = new Date();
    const currentMinutes = now.getHours() * 60 + now.getMinutes();

    const dep = player.currentConnection.departureTime;

    if (dep === currentMinutes) {
        console.log(`The ${ConnectionType[player.currentConnection.type].toUpperCase()} to ${player.currentConnection.endStation.name} is departing now!`);
        player.inMotion = true;
        player.inCity = false;

    } else {
        const hours = Math.floor(dep / 60).toString().padStart(2, '0');
        const minutes = (dep % 60).toString().padStart(2, '0');
        console.log(`Your connection departs at ${hours}:${minutes}. Please wait.`);
    }
};


let traveled = 0;
let scrollOffset = 0;
let speedScale = 1 //meaning 1 update per second
const scrollStep = 0.005; // e.g. scroll after every 0.05 pixels traveled
let lastScrolledAt = 0;

let slowTickTimer = 0;
let slow = 0;



export async function departLoop() {

    if (!player.inMotion || !player.currentConnection) return;

    speedScale = ConnectionSpeeds[player.currentConnection.type] / 60;

    const conn = player.currentConnection;
    const start = conn.startStation.position;
    const end = conn.endStation.position;

    const dx = end[0] - start[0];
    const dy = end[1] - start[1];
    const distance = Math.sqrt(dx * dx + dy * dy); // total distance



    if (player.inMotion && player.currentConnection === conn && traveled < distance) {
        const baseSpeed = ConnectionSpeeds[conn.type];
        const speed = baseSpeed * ((100-slow)/100) //* (0.99 + Math.random() * 0.02); // 99%–101% random


        slowTickTimer--;
        slowTickTimer = Math.max(0,slowTickTimer);
        if(Math.random()*10000<0.5){
            slowTickTimer+=Math.random()*10000
            slow = Math.random()*100
           //console.log("");
        }
        if(slowTickTimer<=0){
            slow=0;
        }


        traveled += speed / (3600 * 20); // speed is in pixels per hour
        const progress = Math.min(traveled / distance, 1);

        // Update position linearly
        const newX = start[0] + dx * progress;
        const newY = start[1] + dy * progress;
        player.position = [newX, newY];

        let currentTerrain: string[];

        const cityTerrain = [
            '🏘️', '🏙️', '🏬', '🏭', '🚦', '🚧', '🚗', '🚌', '🏡', '🚋', '🛤️', '🧍‍♂️', '🧍‍♀️', '🏢', '🏠', '🚕'
        ];

        const fieldsTerrain = [
            '🌾', '🌻', '🪨', '🚜', '🐄', '🐑', '🐓', '🧺', '🌱', '🧑‍🌾', '🍂', '🐎'
        ];


        const forestTerrain = [
            '🌲', '🌳', '🌴', '🦌', '🌿', '🍄', '🦉', '🌰', '🦊', '🕷️', '🦝'
        ];

        const mixedTerrain = [
            '🌾', '🌳', '🌻', '🌴', '🌱', '🦋', '🦜', '🍁', '🐇', '🦨'
        ];

        const arrivalTerrain = [
            '🏙️', '🏠', '🏢', '🚋', '🚶‍♂️', '🧍‍♂️', '🛤️', '🚕', '🚇', '🛑', '🏪', '🚦', '🚎'
        ];


        if (progress < 0.05) {
            currentTerrain = cityTerrain;
        } else if (progress < 0.20) {
            currentTerrain = fieldsTerrain;
        } else if (progress < 0.60) {
            currentTerrain = forestTerrain;
        } else if (progress < 0.75) {
            currentTerrain = mixedTerrain;
        } else {
            currentTerrain = arrivalTerrain;
        }



        const lineLength = 40;
        const scrollingLine = Array.from({ length: lineLength }, (_, i) =>
            currentTerrain[(i + scrollOffset) % currentTerrain.length]
        ).join('');
        if (traveled - lastScrolledAt >= scrollStep) {
            scrollOffset = (scrollOffset + 1) % currentTerrain.length;
            lastScrolledAt = traveled;
        }


      const remaining = distance - traveled;
const etaHours = remaining / speed; // hours

// Get current time
const now = new Date();

// Calculate arrival time by adding remaining time in milliseconds
const arrivalTime = new Date(now.getTime() + etaHours * 3600 * 1000);

const arrivalHours = arrivalTime.getHours().toString().padStart(2, '0');
const arrivalMinutes = arrivalTime.getMinutes().toString().padStart(2, '0');

const arrivalFormatted = `${arrivalHours}:${arrivalMinutes}`;

        // Clear console and print
        console.clear();
        console.log(scrollingLine);
        console.log(`Speed: ${speed.toFixed(1)} p/h | Distance traveled: ${traveled.toFixed(2)} p | Next station: ${player.currentConnection.endStation.name} | Arrival: ${arrivalFormatted}`);
        if(slow>0){
            console.log("Unfortunately this connection will be delayed due to technical issues");
                }
        if((player.currentConnection.departureTime/60+etaHours)>initialArrival+0.05){
            console.log(`Connection is delayed by less than a ${Math.ceil((player.currentConnection.departureTime/60+etaHours)-initialArrival)} hour/s`);
        }
        return;
    } else { // Finish journey
        player.inMotion = false;
        player.city = conn.endStation;
        player.currentConnection = undefined;
        player.inCity = true;
        console.log(`🎉 You have arrived in ${player.city.name}!`);
    }


}