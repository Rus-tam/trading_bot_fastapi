import pandas as pd
from typing import List
from ..websocket.schemas import klineData


def chaikin_osc(confirmed_data: List[klineData]):
    dataframes = []

    for data in confirmed_data:
        data["open"] = float(data["open"])
        data["close"] = float(data["close"])
        data["high"] = float(data["high"])
        data["low"] = float(data["low"])
        data["volume"] = float(data["volume"])
        dataframes.append(pd.DataFrame(data, index=[0]))

    initial_df = pd.concat(dataframes, ignore_index=True)

    df = initial_df.iloc[::-1].reset_index(drop=True)

    # 1. Рассчитать Money Flow Multiplier
    df["mf_multiplier"] = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / (
        df["high"] - df["low"]
    )

    # 2. Рассчитать Money Flow Volume
    df["mf_volume"] = df["mf_multiplier"] * df["volume"]

    # 3. Рассчитать ADL
    df["adl"] = df["mf_volume"].cumsum()

    # 4. Рассчитать EMA для short и long периодов
    short_period = 3
    long_period = 10

    df["ema_short"] = df["adl"].ewm(span=short_period, adjust=False).mean()
    df["ema_long"] = df["adl"].ewm(span=long_period, adjust=False).mean()

    # 5. Рассчитать Chaikin Oscillator
    df["chaikin_oscillator"] = df["ema_short"] - df["ema_long"]

    print(df[["time", "open", "high", "low", "close", "volume", "chaikin_oscillator"]])
