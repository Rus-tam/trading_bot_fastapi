import json
import httpx
import websockets
import pandas as pd
from datetime import datetime, timedelta, timezone
from typing import Optional, Callable
from .schemas import KlineData, KlineInfo
from ..market_processor.service import MarketProcessor


class BinanceService:
    def __init__(self):
        self.websocket_url = "wss://stream.binance.com:443/ws"
        self.connection: Optional[websockets.WebSocketClientProtocol] = None
        self.is_running = False
        self.kline_callback: Optional[Callable[[KlineData], None]] = None
        self.market_processor = MarketProcessor()

    async def connect(self, symbol: str, interval: str):
        params = {
            "method": "SUBSCRIBE",
            "params": [f"{symbol.lower()}@kline_{interval}"],
        }

        try:
            async with websockets.connect(self.websocket_url) as ws:
                await ws.send(json.dumps(params))

                print(
                    f"Подписка на канал с данными по свечам {symbol} c интервалом {interval}"
                )
                print(" ")

                while True:
                    response = await ws.recv()

                    kline = json.loads(response)
                    if "k" in kline:
                        klineInfo = self.parse_kline_data(kline)

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection to Bybit WebSocket closed: {e}")
        except Exception as e:
            print(f"Error in Bybit WebSocket: {e}")

    async def get_historical_kline_data(self, symbol: str, interval: str, limit: int):
        endpoint = "api/v3/klines"

        endTime = int(datetime.utcnow().timestamp() * 1000)
        startTime = endTime - 1000 * 1000 * 60
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "endTime": endTime,
            "startTime": startTime,
            "timeZone": "+5",
            "limit": limit,
        }

        async with httpx.AsyncClient() as client:
            url = f"https://api.binance.com/{endpoint}"
            try:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                result = response.json()
                formatted_result = self.format_historical_kline(result)
                return formatted_result

            except httpx.RequestError as e:
                return {"error": f"Request failed: {str(e)}"}
            except httpx.HTTPStatusError as e:
                return {"error": f"HTTP error: {str(e)}"}

    def parse_kline_data(self, kline: KlineInfo):
        kline_data = {
            "open_time": self._format_time(kline["k"]["t"]),
            "open": float(kline["k"]["o"]),
            "high": float(kline["k"]["h"]),
            "low": float(kline["k"]["l"]),
            "close": float(kline["k"]["c"]),
            "volume": float(kline["k"]["v"]),
            "close_time": self._format_time(kline["k"]["T"]),
            "is_closed": kline["k"]["x"],
            "quote_asset_volume": float(kline["k"]["q"]),
            "number_of_trades": int(kline["k"]["n"]),
            "taker_buy_base_volume": float(kline["k"]["V"]),
            "taker_buy_quote_volume": float(kline["k"]["Q"]),
        }
        return pd.DataFrame(kline_data, index=[0])

    def format_historical_kline(self, row_data):
        formated_klines = []
        for element in row_data:
            formated_klines.append(
                pd.DataFrame(
                    {
                        "open_time": self._format_time(element[0]),
                        "open": float(element[1]),
                        "high": float(element[2]),
                        "low": float(element[3]),
                        "close": float(element[4]),
                        "volume": float(element[5]),
                        "close_time": self._format_time(element[6]),
                        "is_closed": True,
                        "quote_asset_volume": float(element[7]),
                        "number_of_trades": int(element[8]),
                        "taker_buy_base_volume": float(element[9]),
                        "taker_buy_quote_volume": float(element[10]),
                    },
                    index=[0],
                )
            )

        df = pd.concat(formated_klines, ignore_index=True)
        print(" ")
        print("********************")
        print(df["open_time"])
        print("********************")
        print(" ")
        return df

    def _format_time(self, timestamp_ms):
        gmt_offset = timezone(timedelta(hours=5))  # Ваш часовой пояс GMT+5
        utc_time = datetime.fromtimestamp(int(timestamp_ms) / 1000, tz=timezone.utc)
        local_time = utc_time.astimezone(gmt_offset)
        formatted_date = local_time.strftime("%H:%M:%S %d-%m-%Y")

        return formatted_date

    async def server_time(self):
        """
        Получить текущее время сервера Binance.
        Возвращает:
            str: Читаемый формат времени UTC.
        """
        endpoint = "https://api.binance.com/api/v3/time"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(endpoint)
                response.raise_for_status()
                server_time_ms = response.json().get("serverTime")

                # Конвертация времени в UTC
                server_time = datetime.utcfromtimestamp(server_time_ms / 1000)
                return server_time.strftime("%Y-%m-%d %H:%M:%S UTC")
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Failed to fetch server time: {str(e)}")
