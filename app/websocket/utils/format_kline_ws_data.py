from ..schemas import klineData
from datetime import datetime


def format_kline_ws_data(data: klineData):
    return {
        "time": datetime.fromtimestamp(int(data["end"]) / 1000).strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["close"]),
        "volume": float(data["volume"]),
        "turnover": float(data["turnover"]),
    }
