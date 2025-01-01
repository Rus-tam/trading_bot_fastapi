from fastapi import FastAPI
from .core.config import settings
from .modules.binance.controller import BinanceController


app = FastAPI(title=settings.app_name)


binance_controller = BinanceController()
app.include_router(
    binance_controller.router, prefix="/binance", tags=["Binance WebSocket"]
)
