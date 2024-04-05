class HorizontalLedStrip {
    constructor(div){
        this.div = div;
        console.log("jeu cing (lent)");
    }
} 

function main() {
    let root = document.getElementsByTagName("main")[0];
    let d = document.createElement("div");
    d.classList.add("led_strip");
    console.log(root);
    root.appendChild(d);
    new HorizontalLedStrip(d);
}

main();