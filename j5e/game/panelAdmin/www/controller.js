var status_btn = document.querySelector("input[value='Status']");
var play_btn = document.querySelector("input[value='Play']");
var pause_btn = document.querySelector("input[value='Pause']");
var stop_btn = document.querySelector("input[value='Reset']");
var rotation_btn = document.querySelector("input[value='Rotation']");

var txt = document.querySelector("p");

status_btn.addEventListener("click", grid_status);
play_btn.addEventListener("click", play);
pause_btn.addEventListener("click", pause);
stop_btn.addEventListener("click", reset);
rotation_btn.addEventListener("click", rotation);

function grid_status() {
    console.log("État du jeu demandé");
    // TODO: Refactor le fichier pour devenir une classe et pouvoir avoir la grille en paramètre
    // grid.reset();
    fetch("gamemsg?status")
}

function play() {
    txt.textContent = "Jeu en cours";
    fetch("gamemsg?play");
}

function pause() {
    txt.textContent = "Jeu sur pause";
    fetch("gamemsg?pause");
}

function reset() {
    txt.textContent = "Jeu stoppé";
    fetch("gamemsg?reset");
}

function rotation(){
    //ajouter row, col en param
    // fetch("gamemsg?rotation&row="+row"+"&col="+col);
}

// rotation <row> <col> : Changement de sens de rotation d'un anneau à la coordonnée row col.