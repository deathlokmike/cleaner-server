const wsClient = new WebSocket("ws://localhost:8000/ws/client");
let connectionStatus = 'Disconnected';
const statusIndicator = document.createElement('div');


function initializeStatusIndicator() {
    const batteryContainer = document.querySelector('.battery-status');
    statusIndicator.classList.add('status-indicator', 'disconnected');
    statusIndicator.textContent = connectionStatus;
    batteryContainer.parentNode.insertBefore(statusIndicator, batteryContainer);
}

function sendMessage(message) {
    console.log("Sending: " + message);
    wsClient.send(message);
}

function updateConnectionStatus(isConnected) {
    if (isConnected) {
        connectionStatus = 'Connected';
        statusIndicator.classList.remove('disconnected');
        statusIndicator.classList.add('connected');
        statusIndicator.textContent = connectionStatus;
    } else {
        connectionStatus = 'Disconnected';
        statusIndicator.classList.remove('connected');
        statusIndicator.classList.add('disconnected');
        statusIndicator.textContent = connectionStatus;
    }
}

initializeStatusIndicator();

function handleSocketData(data) {
    const noDataPattern = /data:log:vol:-,cur:-,gx:-,gy:-,gz:-,bat:-/;

    if (noDataPattern.test(data)) {
        updateConnectionStatus(false);
    } else {
        updateConnectionStatus(true);
        const logData = event.data.slice(9).split(",");
        const dataMap = {};
        logData.forEach(item => {
            const [key, value] = item.split(":");
            dataMap[key] = value;
        });

        document.getElementById("voltage").textContent = dataMap["vol"] + " V";
        document.getElementById("current").textContent = dataMap["cur"] + " mA";
        document.getElementById("angle").textContent = dataMap["ang"] + "°";
        document.getElementById("front").textContent = dataMap["df"] + " cm";
        document.getElementById("side").textContent = dataMap["ds"] + " cm";

        const batteryLevel = parseInt(dataMap["bat"], 10);
        const batteryIcon = document.getElementById("battery-icon");
        const batteryPercentage = document.getElementById("battery-percentage");
        batteryIcon.style.width = `${batteryLevel}%`;
        batteryPercentage.textContent = `${batteryLevel}%`;

        batteryIcon.classList.remove("battery-full", "battery-medium", "battery-low");
        if (batteryLevel >= 67) {
            batteryIcon.classList.add("battery-full");
        } else if (batteryLevel >= 34) {
            batteryIcon.classList.add("battery-medium");
        } else {
            batteryIcon.classList.add("battery-low");
        }
    }
}

wsClient.onmessage = function(event) {
    const data = event.data;
    if (data.startsWith("data:image")) {
        var imageElement = document.getElementById("image");
        imageElement.src = data;
        imageElement.style.display = "block";
    } else if (data.startsWith("data:log")) {
        handleSocketData(data)
    }
};

const style = document.createElement('style');
style.innerHTML = `
    .status-indicator {
        padding: 5px 10px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        color: #ffffff;
        margin-right: 10px;
    }
    .connected {
        background-color: #4CAF50;
    }
    .disconnected {
        background-color: #F44336;
    }
`;
document.head.appendChild(style);