from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class ChatBase(BaseModel):
    pass

class ChatCreate(ChatBase):
    id: uuid.UUID
    seller_id: uuid.UUID
class ChatUpdate(ChatBase):
    id: uuid.UUID
    buyer_id: uuid.UUID

class ChatRead(ChatBase):
    id: uuid.UUID
    seller_id: uuid.UUID
    buyer_id: Optional[uuid.UUID]

class MessagesBase(BaseModel):
    message: str
    sender_id: uuid.UUID
    chat_id: uuid.UUID
    class Config:
        from_attributes = True

class MessagesCreate(MessagesBase):
    send_at: datetime
    class Config:
        from_attributes = True

class MessagesRead(MessagesBase):
    send_at: datetime
    class Config:
        from_attributes = True
    


