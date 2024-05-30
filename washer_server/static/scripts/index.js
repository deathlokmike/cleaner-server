const ws = new WebSocket("ws://localhost:8000/ws");
const wsImage = new WebSocket("ws://localhost:8000/ws_image");

ws.onmessage = function(event) {
    const message = event.data;
    console.log("Received: " + message);
};

function sendMessage(message) {
    console.log("Sending: " + message);
    ws.send(message);
}

wsImage.onmessage = function(event) {
    var imageElement = document.getElementById("image");
    imageElement.src = event.data;
    imageElement.style.display = "block"; // Показываем изображение после получения данных
};
