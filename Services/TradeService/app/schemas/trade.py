from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class TagBase(BaseModel):
    Description: str = Field(title='Описание', default='')
    GeoTag: dict = Field(title='Гео-тег')

class Tag(TagBase):
    id: int = Field(title='Идентификатор тега', default=None)

class TagCreate(TagBase):
    pass
class Currency(str,Enum):
    Bitcoin = "BTC"
    Matic = "MATIC"
    USDT = "USDT"
class TradeBase(BaseModel):
    #buyer_id: int = Field(title='Идентификатор покупателя')
    #seller_id: int = Field(title='Идентификатор продавца')
    #buyer_address: str = Field(title='Адрес покупателя',default='')
    #seller_address: str = Field(title='Адрес продавца')
    price: int = Field(title='Цена', nullable=False)
    currency: Currency = Field(title='Валюта', nullable=False)
    description: str = Field(title='Описание', default='')
    created_at: str = Field(title='Дата создания', default=datetime.utcnow().isoformat())
    #geo_tag_id: int = Field(title='Идентификатор гео-тега')
    #hide: str = Field(title='Скрыто', nullable=False)

class Trade(TradeBase):
    id: int = Field(title='Идентификатор сделки', default=None)

class TradeCreate(TradeBase):
    pass
