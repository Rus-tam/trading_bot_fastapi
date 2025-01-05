import pandas as pd


class MarketProcessor:
    def __init__(self):
        pass

    def compute_market_indicators(self, df):
        pass

    def chaikin_osc(self, df):
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

        return df
