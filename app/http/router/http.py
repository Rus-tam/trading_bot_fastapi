from fastapi import APIRouter
from ..utils.fetch_bybit_data import fetch_bybit_data
from ..utils.format_kline_data import format_kline_data
from ..schemas import KlineHttpResponse

router = APIRouter(prefix="/bot/v1/http", tags=["HTTP"])


@router.get("/kline")
async def get_kline(symbol: str = "BTCUSDT", interval: str = "1", limit: int = 10):
    endpoint = "/v5/market/kline"
    params = {
        "category": "spot",
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
    }
    data: KlineHttpResponse = await fetch_bybit_data(endpoint, params)

    formatted_data = format_kline_data(data["result"])

    return formatted_data
