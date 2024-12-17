from fastapi import APIRouter
from ..utils.fetch_bybit_data import fetch_bybit_data
from ..utils.format_kline_data import format_kline_data
from ..schemas import KlineHttpResponse

from PyTechnicalIndicators.Bulk.oscillators import chaikin_oscillator

from ...computer.chaikin_osc import chaikin_osc

router = APIRouter(prefix="/bot/v1/http", tags=["HTTP"])


# @router.get("/kline")
# async def get_kline(symbol: str = "BTCUSDT", interval: str = "1", limit: int = 1000):
#     endpoint = "/v5/market/kline"
#     params = {
#         "category": "spot",
#         "symbol": symbol,
#         "interval": interval,
#         "limit": limit,
#     }
#     data: KlineHttpResponse = await fetch_bybit_data(endpoint, params)

#     formatted_data = format_kline_data(data)

#     chaikin_osc(formatted_data)

#     return formatted_data


@router.get("/kline")
async def get_kline(symbol: str = "BTCUSDT", interval: str = "1", limit: int = 25):
    high = []
    low = []
    close = []
    volume = []
    endpoint = "/v5/market/kline"
    params = {
        "category": "spot",
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
    }
    data: KlineHttpResponse = await fetch_bybit_data(endpoint, params)

    formatted_data = format_kline_data(data)

    for elem in formatted_data:
        high.append(elem["high"])
        low.append(elem["low"])
        close.append(elem["close"])
        volume.append(elem["volume"])

    co = chaikin_oscillator(
        high=high,
        low=low,
        close=close,
        volume=volume,
        short_period=3,
        long_period=10,
        moving_average="ema",
    )

    print(co)

    # chaikin_osc(formatted_data)

    return formatted_data
