import base64
from io import BytesIO
from multiprocessing import Queue

from PIL import Image
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from washer_server.services.ml_model import find_person
app = FastAPI()

websocket_clients = []
websocket_image_clients = []
image_queue = Queue()

app.mount("/static", StaticFiles(directory="washer_server/static"), name="static")

templates = Jinja2Templates(directory="washer_server/static/templates")


@app.get("/", response_class=HTMLResponse)
async def get_registration_page(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request,
        },
    )


@app.post("/image")
async def input_request(request: Request):
    image_raw_bytes = await request.body()

    image = Image.frombuffer('RGB', (160, 120), image_raw_bytes, 'raw', 'RGB;16')
    image = image.rotate(angle=270, resample=0, expand=True)

    _ = find_person(image)

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    img_data = f"data:image/png;base64,{img_str}"

    for client in websocket_image_clients:
        await client.send_text(img_data)
    return {"status": "image received"}


@app.websocket("/ws_image")
async def websocket_image_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_image_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        websocket_image_clients.remove(websocket)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            # Forward the message to all connected clients (ESP32s)
            for client in websocket_clients:
                if client != websocket:
                    await client.send_text(data)
    except:
        websocket_clients.remove(websocket)
