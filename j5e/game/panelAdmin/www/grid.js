class Led
{
    constructor(div){
        this.div = div;
        div.classList.add("led");
        this.set_color(0, 200, 0);
    }

    set_color(r, g, b)
    {
        this.div.style.backgroundColor = "rgb("+r+", "+g+", "+b+")";
    }
}

class HorizontalLedStrip {
    constructor(div){
        this.div = div;
        div.classList.add("horizontal_ledstrip");
        div.classList.add("ledstrip");

        // Ajoute les leds
        this.leds = [];
        for (let i=0 ; i<24 ; i++){
            let led_div = document.createElement("div");
            this.div.appendChild(led_div);
            this.leds.push(new Led(led_div));
        }
    }
} 

class VerticalLedStrip {
    constructor(div){
        this.div = div;
        div.classList.add("vertical_ledstrip");
        div.classList.add("ledstrip");

        // Ajoute les leds
        this.leds = [];
        for (let i=0 ; i<24 ; i++){
            let led_div = document.createElement("div");
            this.div.appendChild(led_div);
            this.leds.push(new Led(led_div));
        }
    }
} 

class RingLedStrip {
    constructor(div){
        this.div = div;
        div.classList.add("ring_ledstrip");
        div.classList.add("ledstrip");
        let tds = "<tr>"+("<td></td>".repeat(5)) + "</tr>";
        this.div.innerHTML = "<table>" + tds.repeat(5) + "</table>";
        let table = div.children[0].children[0];
        console.log(table.children[0].children);

        // Setup the leds
        let coordinates = [
            [0, 0], [0, 1],         [0, 3], [0, 4],
            [1, 0],                         [1, 4],
            
            [3, 0],                         [3, 4], 
            [4, 0], [4, 1],         [4, 3], [4, 4]
        ];
        
        // Create leds
        console.log(table.children);
        this.leds = coordinates.map((coords) => {
            return new Led(table.children[coords[0]].children[coords[1]]);
        });
    }
}


class Grid{
    constructor(elt){
        this.table = elt;
        this.table.classList.add("grid");
        let size = 5;
        
        // On créé un tableau capable d'accueillir les ledstrips
        for (let row=0 ; row<size*2-1 ; row++){
            let tr = document.createElement("tr");
            this.table.appendChild(tr);
            
            for (let col=0 ; col<size*2-1 ; col++)
            {
                let td = document.createElement("td");
                tr.appendChild(td);
            }
        }
        
        this.ledStrips = new Array(size*2-1);
        for (let i=0 ; i<this.ledStrips.length ; i++)
            this.ledStrips[i] = new Array(size*2-1);

        // Creation des ledstrips horizontaux (1 ligne sur 2)
        for (let row=0 ; row<size*2-1 ; row+=2){
            this.ledStrips[row] = [];
            for (let col=1 ; col<size*2-1 ; col+=2){
                let td = this.table.children[row].children[col];
                let ledStrip_div = document.createElement("div");
                td.appendChild(ledStrip_div);
                this.ledStrips[row][col] = new HorizontalLedStrip(ledStrip_div);
            }
        }

        // Creation des ledstrips verticaux (1 ligne sur 2 à partir de la 2e ligne)
        for (let row=1 ; row<size*2-1 ; row+=2){
            for (let col=0 ; col<size*2-1 ; col+=2){
                let td = this.table.children[row].children[col];
                let ledStrip_div = document.createElement("div");
                td.appendChild(ledStrip_div);
                this.ledStrips[row][col] = new VerticalLedStrip(ledStrip_div);
            }
        }

        // Creation des leds à toutes les intersections
        for (let row=0 ; row<size*2-1 ; row+=2){
            for (let col=0 ; col<size*2-1 ; col+=2){
                let td = this.table.children[row].children[col];
                let ring_div = document.createElement("div");
                td.appendChild(ring_div);    
                this.ledStrips[row][col] = new RingLedStrip(ring_div);
            }
        }
    }
   
}

function main() {
    let root = document.getElementsByTagName("main")[0];
    let d = document.createElement("table");
    root.appendChild(d);
    new Grid(d);
}

main();