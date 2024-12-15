from fastapi import FastAPI
from .websocket.router import websocket
from .http.router import http


app = FastAPI()

app.include_router(websocket.router)
app.include_router(http.router)
