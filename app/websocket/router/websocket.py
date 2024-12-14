import asyncio
from fastapi import APIRouter, HTTPException
from ..utils.fetch_bybit_info import fetch_bybit_info

router = APIRouter(prefix="/bot/v1/websocket", tags=["Websocket"])

tasks = {}


@router.get("/candles")
async def get_candles(symbol: str = "BTCUSDT", interval: str = "1"):
    """Маршрут для запуска задачи получения свечей"""
    task_id = f"{symbol}_{interval}"
    if task_id in tasks:
        raise HTTPException(status_code=400, detail="Task is already running")

    # Создаем задачу и сохраняем ее в словарь
    task = asyncio.create_task(fetch_bybit_info(symbol, interval))
    tasks[task_id] = task
    print(f"Started task for {symbol} with interval {interval}")
    return {"status": f"Started task for {symbol} with interval {interval}"}


@router.get("/stop_candles")
async def stop_candles(symbol: str = "BTCUSDT", interval: str = "1"):
    """Маршрут для остановки задачи получения свечей"""
    task_id = f"{symbol}_{interval}"
    task = tasks.get(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="No task found for the specified symbol and interval",
        )

    # Отменяем задачу
    task.cancel()
    del tasks[task_id]
    print(f"Stopped task for {symbol} with interval {interval}")
    return {"status": f"Stopped task for {symbol} with interval {interval}"}
