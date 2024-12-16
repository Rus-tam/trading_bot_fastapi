import websockets
import json
from ..schemas import klineData, klineResponse
from ...computer.chaikin_osc import chaikin_osc
import pandas as pd
from .format_kline_ws_data import format_kline_ws_data


async def fetch_bybit_info(symbol: str, interval: str):
    url = "wss://stream.bybit.com/v5/public/linear"
    subscription_params = {"op": "subscribe", "args": [f"kline.{interval}.{symbol}"]}

    confirmed_data = []

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

                    formatted_data = format_kline_ws_data(data)

                    print(formatted_data)
                    print(" ")

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
