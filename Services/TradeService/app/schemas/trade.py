from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

class Currency(str,Enum):
    Bitcoin = "BTC"
    Matic = "MATIC"
    USDT = "USDT"
class Status(str,Enum):
    Create = "Create"
    Pending = "Pending"
    Successful = "Successful"
    Appilation = "Appilation"
    Error = "Error"
    

class TradeBase(BaseModel):
    price: int = Field(title='Цена')
    currency: Currency
    created_at: datetime = Field(title='Дата создания', default=datetime.utcnow())
    

class Trade(TradeBase):
    id: UUID4

class TradeRead(TradeBase):
    id: UUID4
    buyer_address: str
    seller_address: str   
    price: int
    currency: Currency
    description: str
    lat: float
    lon: float
    
class TradeCreate(TradeBase):
    seller_id: uuid.UUID
    price: int
    currency: Currency
    description: str
    lat: float
    lon: float

class TradeAccept(TradeBase):
    buyer_id: uuid.UUID
    buyer_address :str
    currency: Currency
    hide : Status = "Pending"
   
class TradeUpdate(TradeBase):
    buyer_address :str
    price: int
    currency: Currency
    description: str
    lat: float
    lon: float

class TradeUpdateAdmin(TradeBase):
    buyer_id: uuid.UUID
    seller_id: uuid.UUID
    buyer_address: str 
    seller_address: str 
    price: int
    currency: Currency
    description: str
    lat: float
    lon: float
    hide : Status

class TradeDelete(TradeBase):
    ...
