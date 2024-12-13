from fastapi import FastAPI
from .websocket.router import websocket


app = FastAPI()

app.include_router(websocket.router)
