import json
import websockets
import pandas as pd
from typing import Optional, Callable
from .schemas import KlineData, KlineInfo
from ..market_processor.service import MarketProcessor
from .utils import BinanceUtils


class BinanceService:
    def __init__(self):
        self.websocket_url = "wss://stream.binance.com:443/ws"
        self.connection: Optional[websockets.WebSocketClientProtocol] = None
        self.is_running = False
        self.kline_callback: Optional[Callable[[KlineData], None]] = None
        self.market_processor = MarketProcessor()
        self.binance_utils = BinanceUtils()

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
                historical_klines = await self.get_historical_kline_data(
                    symbol=symbol, interval=interval, limit=1000
                )
                while True:
                    response = await ws.recv()

                    kline = json.loads(response)
                    if "k" in kline and kline["k"]["x"] is True:
                        klineInfo = self.parse_kline_data(kline)
                        historical_klines = pd.concat(
                            [historical_klines, klineInfo], ignore_index=True
                        )

                        chaikin = self.market_processor.chaikin_osc(historical_klines)
                        print(" ")
                        print(chaikin)
                        print(" ")

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection to Bybit WebSocket closed: {e}")
        except Exception as e:
            print(f"Error in Bybit WebSocket: {e}")

    async def get_historical_kline_data(self, symbol: str, interval: str, limit: int):
        url = "https://api.binance.com/api/v3/klines"

        kline_data = await self.binance_utils.get_bybit_kline(
            url, symbol=symbol, interval=interval, limit=limit
        )

        return kline_data

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
