
let status_update = new EventSource('/abonnementSSE');

let status_observers = [];

status_update.onmessage = function(event) {
    const message = event.data;
    for (let observer of status_observers) {
        observer(message);
    }
    // console.log("Message from server:", message);
    // Mettre à jour l'interface utilisateur en fonction du message
};

status_update.onerror = function(error) {
    console.error("SSE error:", error);

    // Fermer la connexion SSE et tenter de la rouvrir
    status_update.close();
    setTimeout(function() {
        status_update = new EventSource('/abonnementSSE');
    }, 100);
};

// Fermer la connexion SSE lorsque la page est déchargée
window.addEventListener('beforeunload', function() {
    status_update.close();
});
