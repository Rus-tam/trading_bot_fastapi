from pydantic import BaseModel
from typing import List


class klineData(BaseModel):
    start: int
    end: int
    interval: str
    open: str
    close: str
    high: str
    low: str
    volume: str
    turnover: str
    confirm: bool
    timestamp: int


class klineResponse(BaseModel):
    topic: str
    data: List[klineData]
    ts: int
    type: str
