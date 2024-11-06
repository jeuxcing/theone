
function main() {
    // Création de la grille
    let root = document.getElementsByTagName("main")[0];
    let d = document.createElement("table");
    root.appendChild(d);
    let grid = new Grid(d);
    
    // Création du moteur Vue
    let vue_engine = new VueEngine(grid);
    // Enregistrement du moteur Vue pour les messages du serveur
    let wrap_function = function(msg){
        vue_engine.parse_msg(msg);
    };
    status_observers.push(wrap_function);

    return [grid, vue_engine];
}

let grid, vue_engine = main();