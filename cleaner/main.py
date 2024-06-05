from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from cleaner.controllers.images import router as image_router
from cleaner.controllers.pages import router as pages_router
from cleaner.controllers.websockets import router as websockets_router

app = FastAPI()
app.include_router(image_router)
app.include_router(websockets_router)
app.include_router(pages_router)

app.mount("/static", StaticFiles(directory="cleaner/static"), name="static")
