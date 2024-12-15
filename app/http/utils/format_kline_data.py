from ..schemas import KlineHttpResult
from datetime import datetime


def format_kline_data(data: KlineHttpResult):
    formatted_list = []
    list = data["list"]

    for elem in list:
        formatted_list.append(
            {
                "startTime": datetime.fromtimestamp(int(elem[0]) / 1000).strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                "openPrice": float(elem[1]),
                "highPrice": float(elem[2]),
                "lowPrice": float(elem[3]),
                "closePrice": float(elem[4]),
                "volume": float(elem[5]),
                "turnover": float(elem[6]),
            }
        )

    return formatted_list
