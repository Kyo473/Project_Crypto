from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime

class TagBase(BaseModel):
    Description: str = Field(title='Описание', default='')
    GeoTag: dict = Field(title='Гео-тег')

class Tag(TagBase):
    id: int = Field(title='Идентификатор тега', default=None)

class TagCreate(TagBase):
    pass

class TradeBase(BaseModel):
    #buyer_id: int = Field(title='Идентификатор покупателя')
    #seller_id: int = Field(title='Идентификатор продавца')
    #buyer_address: str = Field(title='Адрес покупателя',default='')
    #seller_address: str = Field(title='Адрес продавца')
    price: int = Field(title='Цена', nullable=False)
    currency: str = Field(title='Валюта', nullable=False)
    description: str = Field(title='Описание', default='')
    #created_at: Any = Field(title='Дата создания', default=datetime.utcnow)
    #geo_tag_id: int = Field(title='Идентификатор гео-тега')
    #hide: str = Field(title='Скрыто', nullable=False)

class Trade(TradeBase):
    id: int = Field(title='Идентификатор сделки', default=None)

class TradeCreate(TradeBase):
    pass
