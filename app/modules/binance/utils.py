import httpx
import pandas as pd
from datetime import datetime, timedelta, timezone


class BinanceUtils:
    def __init__(self):
        pass

    async def _fetch_data(self, url, params):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                result = response.json()
                return result

            except httpx.RequestError as e:
                return {"error": f"Request failed: {str(e)}"}
            except httpx.HTTPStatusError as e:
                return {"error": f"HTTP error: {str(e)}"}

    async def get_bybit_kline(self, url, symbol="BTCUSDT", interval="1", limit=25):
        params = {
            "symbol": symbol,
            "interval": interval,
            "timeZone": "+5",
            "limit": limit,
        }
        data = await self._fetch_data(url, params)
        formatted_data = self._format_historical_kline(data)
        return formatted_data

    def _format_time(self, timestamp_ms):
        gmt_offset = timezone(timedelta(hours=5))
        utc_time = datetime.fromtimestamp(int(timestamp_ms) / 1000, tz=timezone.utc)
        local_time = utc_time.astimezone(gmt_offset)
        formatted_date = local_time.strftime("%H:%M:%S %d-%m-%Y")

        return formatted_date

    def _format_historical_kline(self, row_data):
        formated_klines = []
        for element in row_data:
            formated_klines.append(
                pd.DataFrame(
                    {
                        "open_time": datetime.fromtimestamp(
                            int(element[0]) / 1000
                        ).strftime("%d-%m-%Y %H:%M:%S"),
                        "open": float(element[1]),
                        "high": float(element[2]),
                        "low": float(element[3]),
                        "close": float(element[4]),
                        "volume": float(element[5]),
                        "close_time": datetime.fromtimestamp(
                            int(element[6]) / 1000
                        ).strftime("%d-%m-%Y %H:%M:%S"),
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

        return df

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
