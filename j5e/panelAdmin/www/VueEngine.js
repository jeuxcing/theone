
class VueEngine {
    constructor(grid) {
        this.grid = grid;
    }

    parse_msg(msg) {
        // charge le message dans un objet json
        let json = JSON.parse(msg);

        // Si le message est une action, traite l'action
        if (json.action)
        {
            this.parse_action(json);
        }

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
        let row = element.coords.row;
        let col = element.coords.col;
        let segtype = element.coords.segtype;
        let offset = element.coords.offset;
        let color = element.type.toLowerCase();

        this.grid.set_color(row, col, segtype, offset, color);
    }

    parse_action(json) {
        let action = json.action;
        
        switch (action) {
            case "level_completed":
            case "level_failed":
                this.grid.reset();
                break;
        }
    }
}

