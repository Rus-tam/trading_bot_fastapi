import pandas as pd


class MarketProcessor:
    def __init__(self):
        pass

    def compute_market_indicators(self, df):
        pass

    def chaikin_osc(self, data):
        if len(data) > 1005:
            data = data[5:]

        df = pd.DataFrame([item for item in data])

        # 1. Рассчитать Money Flow Multiplier
        df["mf_multiplier"] = (
            (df["close"] - df["low"]) - (df["high"] - df["close"])
        ) / (df["high"] - df["low"])

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
        df["chaikin_osc"] = df["ema_short"] - df["ema_long"]

        return df, data

    def rsi(self, df, period=14):
        # Разница между текущей и предыдущей ценой закрытия
        df["delta"] = df["close"].diff()
        # Приросты (положительные изменения)
        df["gain"] = df["delta"].where(df["delta"] > 0, 0)

        # Потери (отрицательные изменения)
        df["loss"] = -df["delta"].where(df["delta"] < 0, 0)

        # Скользящее среднее приростов и потерь
        df["avg_gain"] = df["gain"].rolling(window=period, min_periods=1).mean()
        df["avg_loss"] = df["loss"].rolling(window=period, min_periods=1).mean()

        # Отношение приростов к потерям
        df["rs"] = df["avg_gain"] / df["avg_loss"]
        df["RSI"] = 100 - (100 / (1 + df["rs"]))  # Формула RSI

        return df

    def sma(self, df, period=9):
        df["SMA"] = df["close"].rolling(window=period).mean()

        return df

    def macd(self, df, short_window=12, long_window=26, signal_window=9):
        df["EMA_short"] = df["close"].ewm(span=short_window, adjust=False).mean()
        df["EMA_long"] = df["close"].ewm(span=long_window, adjust=False).mean()

        df["MACD"] = df["EMA_short"] - df["EMA_long"]
        df["Signal_Line"] = df["MACD"].ewm(span=signal_window, adjust=False).mean()
        df["Histogram"] = df["MACD"] - df["Signal_Line"]

        return df
