import websockets
import json
from ..schemas import klineData, klineResponse
from ...computer.chaikin_osc import chaikin_osc
import pandas as pd
from .format_kline_ws_data import format_kline_ws_data
from ...http.utils.fetch_bybit_data import fetch_bybit_data
from ...http.utils.format_kline_data import format_kline_data


async def fetch_bybit_info(symbol: str, interval: str):
    url = "wss://stream.bybit.com/v5/public/linear"
    subscription_params = {"op": "subscribe", "args": [f"kline.{interval}.{symbol}"]}

    confirmed_data = []
    first_timestamp = 0
    start_time = 0
    end_time = 0
    kline_data_historical = []

    try:
        async with websockets.connect(url) as ws:
            await ws.send(json.dumps(subscription_params))
            print(f"Subscribed to kline data for {symbol} {interval}")
            counter = 0

            while True:
                response = await ws.recv()

                klineInfo: klineResponse = json.loads(response)

                if "data" in klineInfo:
                    data: klineData = klineInfo["data"][0]

                    if data["confirm"]:
                        formatted_data = format_kline_ws_data(data)

                        # Вычисления временных отрезков для произведения http запроса
                        if first_timestamp == 0:
                            first_timestamp = data["end"]
                            start_time = first_timestamp - 1000 * 60000
                            end_time = first_timestamp - 60000

                            endpoint = "/v5/market/kline"
                            params = {
                                "category": "spot",
                                "symbol": symbol,
                                "interval": interval,
                                "start": start_time,
                                "end": end_time,
                                "limit": 1000,
                            }

                            historical_kline = await fetch_bybit_data(endpoint, params)

                            print(historical_kline["result"]["list"])

                    # if data["confirm"]:
                    #     confirmed_data.append(data)
                    #     counter += 1
                    #     print(f"Counter: {counter}")
                    #     print(" ")
                    #     df = pd.DataFrame(data, index=[0])
                    #     print(
                    #         df[
                    #             [
                    #                 "open",
                    #                 "high",
                    #                 "low",
                    #                 "close",
                    #                 "volume",
                    #             ]
                    #         ]
                    #     )
                    #     if len(confirmed_data) >= 10:
                    #         pass
                    #         chaikin_osc(confirmed_data)
                    # else:
                    #     pass

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection to Bybit WebSocket closed: {e}")
    except Exception as e:
        print(f"Error in Bybit WebSocket: {e}")
