
class VueEngine {
    constructor(grid) {
        this.grid = grid;
    }

    parse_msg(msg) {
        console.log(msg);
        // charge le message dans un objet json
        let json = JSON.parse(msg);

        // Parcours les éléments au sein du json pour mettre à jour la grille
        for (let elem in json.elements)
        {
            let element = json.elements[elem];
            this.parse_element(element);
        }
        for (let elem in json.agents)
        {
            let element = json.agents[elem];
            this.parse_element(element);
        }
    }

    parse_element(element) {
        let row = element.row;
        let col = element.col;
        let segtype = element.segtype;
        let offset = element.offset;
        let color = element.type.toLowerCase();

        console.log(row, col, segtype, offset, color);
        this.grid.set_color(row, col, segtype, offset, color);
    }
}

