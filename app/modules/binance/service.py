import json
import websockets
from typing import Optional, Callable
from .schemas import KlineData, KlineInfo


class BinanceService:
    def __init__(self):
        self.websocket_url = "wss://stream.binance.com:443/ws"
        self.connection: Optional[websockets.WebSocketClientProtocol] = None
        self.is_running = False
        self.kline_callback: Optional[Callable[[KlineData], None]] = None

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
                        print(" ")
                        print(klineInfo)

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection to Bybit WebSocket closed: {e}")
        except Exception as e:
            print(f"Error in Bybit WebSocket: {e}")

    def parse_kline_data(self, kline: KlineInfo):
        return KlineData(
            open_time=kline["k"]["t"],
            open=float(kline["k"]["o"]),
            high=float(kline["k"]["h"]),
            low=float(kline["k"]["l"]),
            close=float(kline["k"]["c"]),
            volume=float(kline["k"]["v"]),
            close_time=kline["k"]["T"],
            is_closed=kline["k"]["x"],
            quote_asset_volume=float(kline["k"]["q"]),
            number_of_trades=kline["k"]["n"],
            taker_buy_base_volume=float(kline["k"]["V"]),
            taker_buy_quote_volume=float(kline["k"]["Q"]),
        )
