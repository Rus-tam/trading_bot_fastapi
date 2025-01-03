import asyncio
from fastapi import APIRouter, HTTPException
from .service import BinanceService


class BinanceController:
    def __init__(self):
        self.router = APIRouter()
        self.binance_service = BinanceService()
        self.tasks = {}

        # Определяем маршруты
        self.router.post("/get_candles")(self.get_candles)
        self.router.post("/disconnect")(self.stop_candles)
        self.router.get("/http_klines")(self.http_klines)
        self.router.get("/server_time")(self.server_time)

    async def get_candles(self, symbol: str = "BTCUSDT", interval: str = "1m"):
        task_id = f"{symbol}_{interval}"
        if task_id in self.tasks:
            raise HTTPException(status_code=400, detail="Task is already running")
        task = asyncio.create_task(self.binance_service.connect(symbol, interval))
        self.tasks[task_id] = task
        print(f"Получаю данные по свечам для пары {symbol} с интервалом {interval}")
        return {"status": f"Started task for {symbol} with interval {interval}"}

    async def stop_candles(self, symbol: str = "BTCUSDT", interval: str = "1m"):
        """Маршрут для остановки задачи получения свечей"""
        task_id = f"{symbol}_{interval}"
        task = self.tasks.get(task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="No task found for the specified symbol and interval",
            )

        # Отменяем задачу
        task.cancel()
        del self.tasks[task_id]
        print(
            f"Прекращаю получение данных по свечам для пары {symbol} с интервалом {interval}"
        )
        return {"status": f"Stopped task for {symbol} with interval {interval}"}

    async def http_klines(
        self, symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 5
    ):
        await self.binance_service.get_historical_kline_data(
            symbol=symbol, interval=interval, limit=limit
        )

    async def server_time(self):
        server_time = await self.binance_service.server_time()

        return server_time
