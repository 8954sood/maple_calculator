from pydantic import BaseModel
from datetime import date
from typing import Literal

class TradeCreate(BaseModel):
    type: Literal["sell", "buy"]
    title: str
    quantity: int
    price: int
    price_unit: int  # 1 또는 10000
    date: date

class TradeRead(BaseModel):
    id: int
    type: str
    title: str
    quantity: int
    price: int
    price_unit: int
    date: date

    class Config:
        orm_mode = True 