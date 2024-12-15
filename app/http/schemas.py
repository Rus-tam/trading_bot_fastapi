from pydantic import BaseModel
from typing import List


class KlineHttpResult(BaseModel):
    category: str
    symbol: str
    list: List[List[str]]


class KlineHttpResponse(BaseModel):
    retCode: str
    retMsg: str
    result: KlineHttpResult
