
const status_update = new EventSource('/gameStatus');
console.log("J'ai bien chargé");

status_update.onmessage = function(event) {
    const message = event.data;
    console.log("Message from server:", message);
    // Mettre à jour l'interface utilisateur en fonction du message
};

status_update.onerror = function(error) {
    console.error("SSE error:", error);
};
