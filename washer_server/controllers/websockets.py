from fastapi import WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter

from washer_server.services.connection_manager import (ConnectionType,
                                                       connection_manager)

router = APIRouter(prefix="/ws")


@router.websocket("/client")
async def websocket_image_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket, ConnectionType.client)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_message_to_cleaner(data)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)


@router.websocket("/cleaner")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket, ConnectionType.cleaner)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
