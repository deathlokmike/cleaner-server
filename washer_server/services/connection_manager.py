from dataclasses import dataclass
from enum import Enum
from typing import Optional

from fastapi import WebSocket


class ConnectionType(Enum):
    cleaner = 0
    client = 1


class CleanerStatus(Enum):
    launched = "launched"
    stopped = "stopped"
    suspended = "suspended"


@dataclass
class Cleaner:
    mac_address: Optional[str] = None
    status: CleanerStatus = CleanerStatus.stopped


class ConnectionManager:
    def __init__(self):
        self._cleaners: list[WebSocket] = []
        self.clients: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, type_: ConnectionType):
        await websocket.accept()
        if type_ == ConnectionType.cleaner:
            self._cleaners.append(websocket)
        elif type_ == ConnectionType.client:
            self.clients.append(websocket)

    async def send_message_to_cleaner(self, data: str):
        for client in self._cleaners:
            print(f"Message to cleaner: {data}")
            await client.send_text(data)

    async def send_image_to_client(self, formatted_img: str):
        for client in self.clients:
            await client.send_text(formatted_img)

    def disconnect(self, websocket: WebSocket):
        self._cleaners.remove(websocket)
        self.clients.remove(websocket)


connection_manager = ConnectionManager()
