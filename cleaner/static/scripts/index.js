const wsImage = new WebSocket("ws://localhost:8000/ws/client");


function sendMessage(message) {
    console.log("Sending: " + message);
    wsImage.send(message);
}

wsImage.onmessage = function(event) {
    var imageElement = document.getElementById("image");
    imageElement.src = event.data;
    imageElement.style.display = "block";
};
