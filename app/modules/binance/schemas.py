from pydantic import BaseModel
from typing import Union, Optional


class Kline(BaseModel):
    t: int  # Kline start time
    T: int  # Kline close time
    s: str  # Symbol
    i: str  # Interval
    f: int  # First trade ID
    L: int  # Last trade ID
    o: str  # Open price
    c: str  # Close price
    h: str  # High price
    l: str  # Low price
    v: str  # Base asset volume
    n: int  # Number of trades
    x: bool  # Is this kline closed
    q: str  # Quote asset volume
    V: str  # Taker buy base asset volume
    Q: str  # Taker buy quote asset volume
    B: str  # Ignore


class KlineInfo(BaseModel):
    e: str
    E: int
    s: str
    k: Kline


class KlineData(BaseModel):
    open_time: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time: str
    is_closed: bool
    quote_asset_volume: float
    number_of_trades: int
    taker_buy_base_volume: float
    taker_buy_quote_volume: float


class ServerTimeResponce(BaseModel):
    serverTime: int
