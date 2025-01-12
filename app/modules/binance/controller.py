import asyncio
from fastapi import APIRouter, HTTPException
from .service import BinanceService
from .schemas import ServerTimeResponce


class BinanceController:
    def __init__(self):
        self.router = APIRouter()
        self.binance_service = BinanceService()
        self.tasks = {}

        # Определяем маршруты
        self.router.get("/get_candles")(self.get_candles)
        self.router.get("/disconnect")(self.stop_candles)
        self.router.get("/server_time")(self.server_time)
        self.router.get("/account_info")(self.account_info)

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

    async def server_time(self) -> ServerTimeResponce:
        try:
            return await self.binance_service.get_server_time()
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def account_info(self):
        await self.binance_service.get_account_info()
        # try:
        #     return await self.binance_service.get_account_info()
        # except RuntimeError as e:
        #     raise HTTPException(status_code=500, detail=str(e))
