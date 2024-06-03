from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from washer_server.controllers.images import router as image_router
from washer_server.controllers.pages import router as pages_router
from washer_server.controllers.websockets import router as websockets_router

app = FastAPI()
app.include_router(image_router)
app.include_router(websockets_router)
app.include_router(pages_router)

app.mount("/static", StaticFiles(directory="washer_server/static"), name="static")
