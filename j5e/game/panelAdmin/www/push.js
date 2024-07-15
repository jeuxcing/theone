
const eventSource = new EventSource('/stream');

eventSource.onmessage = function(event) {
    const message = event.data;
    console.log("Message from server:", message);
    // Mettre à jour l'interface utilisateur en fonction du message
};

eventSource.onerror = function(error) {
    console.error("SSE error:", error);
};
