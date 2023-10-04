from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from enum import Enum
from typing import Optional
class Currency(str,Enum):
    Bitcoin = "BTC"
    Matic = "MATIC"
    USDT = "USDT"
class Hide(str,Enum):
    Open = "Open"
    Close = "Close"
    

class TradeBase(BaseModel):
    #buyer_id: int = Field(title='Идентификатор покупателя')
    #seller_id: int = Field(title='Идентификатор продавца')
    #buyer_address: str = Field(title='Адрес покупателя',default='')
    #seller_address: str = Field(title='Адрес продавца')
    price: int = Field(title='Цена')
    currency: Currency = Field(title='Валюта')
    description: Optional[str] = ''
    created_at: datetime = Field(title='Дата создания', default=datetime.utcnow())
    lat: float
    lon: float
    hide: Hide = Field(title='Скрыто', default='Open')

class Trade(TradeBase):
    id: UUID4 = Field(title='Идентификатор сделки', default=None)

class TradeCreate(TradeBase):
    price: int
    currency: Currency
    description: str
    lat: float
    lon: float

class TradeUpdate(TradeBase):
    price: int
    currency: Currency
    description: str
    lat: float
    lon: float

class TradeDelete(TradeBase):
    ...
