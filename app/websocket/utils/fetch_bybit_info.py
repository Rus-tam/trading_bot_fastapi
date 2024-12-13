import websockets
import json


async def fetch_bybit_info(symbol: str, interval: str):
    """Подключение к Bybit WebSocket API и вывод данных в консоль"""
    url = "wss://stream.bybit.com/v5/public/linear"
    subscription_params = {"op": "subscribe", "args": [f"kline.{interval}.{symbol}"]}

    try:
        async with websockets.connect(url) as ws:
            await ws.send(json.dumps(subscription_params))
            print(f"Subscribed to kline data for {symbol} {interval}")

            while True:
                response = await ws.recv()
                data = json.loads(response)

                print(" ")
                print(data)
                print(" ")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection to Bybit WebSocket closed: {e}")
    except Exception as e:
        print(f"Error in Bybit WebSocket: {e}")
