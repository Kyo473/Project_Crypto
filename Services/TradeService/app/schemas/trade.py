from pydantic import BaseModel, UUID4
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
    class Config:
        from_attributes = True
    

class Trade(TradeBase):
    id: UUID4

class TradeRead(TradeBase):
    id: uuid.UUID
    buyer_address: str
    seller_address: str   
    price: float
    currency: Currency
    created_at: datetime
    description: str
    lat: float
    lon: float
    hide: Status
    
class TradeCreate(TradeBase):
    seller_id: uuid.UUID
    seller_address: str   
    price: float
    currency: Currency
    description: str
    lat: float
    lon: float
    hide: Status

class TradeAccept(TradeBase):
    buyer_id: uuid.UUID
    buyer_address :str
    hide : Status = "Pending"
   
class TradeUpdate(TradeBase):
    buyer_address :str
    price: float
    currency: Currency
    description: str
    lat: float
    lon: float
    
class TradeUpdateAdmin(TradeBase):
    buyer_id: uuid.UUID
    seller_id: uuid.UUID
    buyer_address: str 
    seller_address: str 
    price: float
    currency: Currency
    description: str
    lat: float
    lon: float
    hide : Status

class TradeDelete(TradeBase):
    buyer_id: uuid.UUID
    seller_id: uuid.UUID
    buyer_address: str 
    seller_address: str 
    price: float
    currency: Currency
    created_at: datetime
    description: str
    lat: float
    lon: float
    hide : Status
