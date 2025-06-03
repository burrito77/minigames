// consoleCommands.ts

import { Connection, ConnectionType } from "./Connection";
import { player } from "./Generator";



type CommandFunction = (...args: string[]) => void;

class ConsoleCommandHandler {
    private commands: Map<string, CommandFunction> = new Map();

    constructor() {
        this.registerDefaultCommands();
    }

    private registerDefaultCommands() {
        this.register("help", this.help);
        this.register("echo", this.echo);
        this.register("clear", this.clear);
        this.register("city", this.city);
        this.register("station", this.station);
        this.register("hop", this.hop);
        this.register("out",this.out)
    }

    public register(command: string, handler: CommandFunction) {
        this.commands.set(command.toLowerCase(), handler);
    }

    public execute(input: string) {
        const [command, ...args] = input.trim().split(/\s+/);
        const handler = this.commands.get(command.toLowerCase());

        if (handler) {
            handler(...args);
        } else {
            console.log(`Unknown command: ${command}`);
        }
    }

    private help = () => {
        console.log("Available commands:");
        for (const cmd of this.commands.keys()) {
            console.log(` - ${cmd}`);
        }
    };

    private echo = (...args: string[]) => {
        console.log(args.join(" "));
    };

    private clear = () => {
        console.clear();
    };

    private city = () => {
        if (player.inCity) {
            if (player.city.size > 0.7) {
                console.log(`you are in huge city called ${player.city.name}, from here you can travel to another ${player.city.connectedCities.length} localities`);
                return;
            }
            if (player.city.size > 0.5) {
                console.log(`Welcome in town of ${player.city.name} located just near X:${player.city.position[0]}`)
            } else {
                console.log(`Welcome in beatiful village ${player.city.name}`)
            }

        } else {
            console.log("you are not in any locality")
        }

    }

    private station = () => {
        if (!player.inCity || !player.city) {
            console.log("You are not in any locality.");
            return;
        }

        const connections = player.city.connections as Connection[];

        if (!connections || connections.length === 0) {
            console.log("There are no departures from this station.");
            return;
        }

        const now = new Date();
        const currentMinutes = now.getHours() * 60 + now.getMinutes();

        const departures = connections
            .filter(conn => conn.startStation === player.city)
            .sort((a, b) => a.departureTime - b.departureTime);

        if (departures.length === 0) {
            console.log("There are no departures from this station.");
            return;
        }

        console.log(" # | HH:MM |         ENDCITY         |  TYPE  ");
        console.log("----|--------|--------------------------|--------");

        let nextHighlighted = false;

        for (let i = 0; i < departures.length; i++) {
            const conn = departures[i];
            const hours = Math.floor(conn.departureTime / 60).toString().padStart(2, '0');
            const minutes = (conn.departureTime % 60).toString().padStart(2, '0');
            const timeStr = `${hours}:${minutes}`;

            const endCityName = conn.endStation.name.padEnd(24, ' ');
            const typeStr = ConnectionType[conn.type].toUpperCase().padEnd(6, ' ');

            const indexStr = i.toString().padStart(2, ' ');
            const prefix = (!nextHighlighted && conn.departureTime > currentMinutes) ? '-->' : '   ';

            if (!nextHighlighted && conn.departureTime > currentMinutes) {
                nextHighlighted = true;
            }

            console.log(`${prefix}${indexStr} | ${timeStr} | ${endCityName} | ${typeStr}`);
        }
    };

    private hop = () => {
        if (!player.inCity || !player.city) {
            console.log("You are not in any locality.");
            return;
        }

        const connections = player.city.connections as Connection[];
        if (!connections || connections.length === 0) {
            console.log("There are no departures from this station.");
            return;
        }

        const now = new Date();
        const currentMinutes = now.getHours() * 60 + now.getMinutes();

        const nextConnection = connections
            .filter(conn => conn.startStation === player.city && conn.departureTime > currentMinutes)
            .sort((a, b) => a.departureTime - b.departureTime)[0];

        if (nextConnection) {
            player.sitOnConnection(nextConnection);
            console.log(`You hopped on the ${ConnectionType[nextConnection.type].toUpperCase()} to ${nextConnection.endStation.name} departing at ${Math.floor(nextConnection.departureTime / 60).toString().padStart(2, '0')}:${(nextConnection.departureTime % 60).toString().padStart(2, '0')}.`);
        } else {
            console.log("There are no upcoming departures from this station today.");
        }
    };

    private out = ()=>{
        if(player.inMotion){
            console.log("you are riding the train and are unable hop off! use 'forceout' but be careful - you might get stranded");
        }
        player.currentConnection = undefined;
        console.log("You left the train");
    }
}

export const ConsoleHandler = new ConsoleCommandHandler();