import { cities, generateCities, generateConnectingCities, generateConnections, generatePlayer, player, printCities, printConnectedCities, printConnections } from "./Generator";
import * as readline from 'readline';
import { ConsoleHandler } from './Console'; // adjust the path as needed
import { Player } from "./Player";
import { awaitDeparture, departLoop } from "./asyncEventCheck";
import { Connection, ConnectionType } from "./Connection";


generateCities(1000,50);
console.log("Cities loaded");
generateConnectingCities();
console.log("Cities connected");
generateConnections(100);
console.log("Connections generated");
generatePlayer()


setInterval(awaitDeparture, 10000);
setInterval(departLoop, 50);


player.city.connections.push(new Connection(player.city,cities[1],[],ConnectionType.ic,982))

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: '> '
});

console.log("use help maybe?");
rl.prompt();

rl.on('line', (line) => {
    ConsoleHandler.execute(line);
    rl.prompt();
}).on('close', () => {
    console.log('Exiting console.');
    process.exit(0);
});


