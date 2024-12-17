import pandas as pd
import numpy as np
from ..websocket.schemas import klineData
from typing import List


def calculate_rsi(data: List[klineData], period: int = 14):
    dataframes = []

    for data in data:
        data["open"] = float(data["open"])
        data["close"] = float(data["close"])
        data["high"] = float(data["high"])
        data["low"] = float(data["low"])
        data["volume"] = float(data["volume"])
        dataframes.append(pd.DataFrame(data, index=[0]))

    initial_df = pd.concat(dataframes, ignore_index=True)

    df = initial_df.iloc[::-1].reset_index(drop=True)

    df["delta"] = df[
        "close"
    ].diff()  # Разница между текущей и предыдущей ценой закрытия

    df["gain"] = df["delta"].where(
        df["delta"] > 0, 0
    )  # Приросты (положительные изменения)
    df["loss"] = -df["delta"].where(
        df["delta"] < 0, 0
    )  # Потери (отрицательные изменения)

    # Скользящее среднее приростов и потерь
    df["avg_gain"] = df["gain"].rolling(window=period, min_periods=1).mean()
    df["avg_loss"] = df["loss"].rolling(window=period, min_periods=1).mean()

    # Отношение приростов к потерям
    df["rs"] = df["avg_gain"] / df["avg_loss"]
    df["RSI"] = 100 - (100 / (1 + df["rs"]))  # Формула RSI

    print(df[["RSI"]])
