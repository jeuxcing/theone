// rotation <row> <col> : Changement de sens de rotation d'un anneau à la coordonnée row col.

class Controller {
    constructor(grid) {
        this.grid = grid;
        this.get_html_items();
    }

    get_html_items() {
        this.status_btn = document.querySelector("input[id='statusButton']");
        this.play_btn = document.querySelector("input[id='playButton']");
        this.pause_btn = document.querySelector("input[id='pauseButton']");
        this.reset_btn = document.querySelector("input[id='resetButton']");
        this.rotation_btn = document.querySelector("input[id='rotationButton']");
        this.lvl_btn = document.querySelector("input[id='lvlButton']");

        this.txt = document.querySelector("p");
        
        this.lvl_idx = document.querySelector("input[id='lvl']");
        this.row = document.querySelector("input[id='row']");
        this.col = document.querySelector("input[id='col']");


        let that = this;
        // ATTENTION : Pour toute NOUVELLE commande, penser à ajouter le nom de la commande dans AdminFlask

        let grid_status = () => {
            console.log("État du jeu demandé");
            that.grid.reset();
            fetch("gamemsg?status")
        };

        let play = () => {
            that.txt.textContent = "Jeu en cours";
            fetch("gamemsg?play");
        };

        let pause = () => {
            that.txt.textContent = "Jeu sur pause";
            fetch("gamemsg?pause");
        };

        let reset = () => {
            that.txt.textContent = "Jeu stoppé";
            that.grid.reset();
            fetch("gamemsg?reset");
        };

        let rotation = () => {
            console.log("Not implemented yet");
            let row = parseInt(that.row.value);
            let col = parseInt(that.col.value);
            fetch("gamemsg?rotation&row="+row+"&"+"col="+col);
        };

        let load_lvl = () => {
            let idx = parseInt(that.lvl_idx.value);
            fetch("gamemsg?load_lvl&idx="+idx);
        };

        this.status_btn.addEventListener("click", grid_status);
        this.play_btn.addEventListener("click", play);
        this.pause_btn.addEventListener("click", pause);
        this.reset_btn.addEventListener("click", reset);
        this.rotation_btn.addEventListener("click", rotation);
        this.lvl_btn.addEventListener("click", load_lvl);    
    }
}