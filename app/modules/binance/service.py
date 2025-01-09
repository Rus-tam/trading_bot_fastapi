import json
import websockets
from typing import Optional, Callable
from .schemas import KlineData
from ..market_processor.service import MarketProcessor
from .utils import BinanceUtils


class BinanceService:
    def __init__(self):
        self.websocket_url = "wss://stream.binance.com:443/ws"
        self.http_url = "https://api.binance.com/api/v3/klines"
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

        historical_klines = await self.get_historical_kline_data(
            symbol=symbol, interval=interval, limit=1000
        )

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
                    if "k" in kline and kline["k"]["x"] is True:
                        klineInfo = self.binance_utils._parse_kline_data(kline)
                        historical_klines.append(klineInfo)

                        chaikin, historical_klines = self.market_processor.chaikin_osc(
                            historical_klines
                        )

                        rsi = self.market_processor.rsi(chaikin, period=14)

                        sma = self.market_processor.sma(rsi, period=9)

                        macd = self.market_processor.macd(
                            sma, short_window=12, long_window=26, signal_window=9
                        )

                        print(" ")
                        print("**************************")
                        print(
                            macd[
                                [
                                    "close_time",
                                    "open",
                                    "close",
                                    "volume",
                                    "chaikin_osc",
                                    "RSI",
                                    "SMA",
                                    "MACD",
                                    "Signal_Line",
                                    "Histogram",
                                ]
                            ]
                        )

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
