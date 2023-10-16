from pydantic import BaseModel, UUID4
from datetime import datetime
import uuid

class ChatBase(BaseModel):
    pass

class ChatCreate(ChatBase):
    seller_id: uuid.UUID
    buyer_id: uuid.UUID

class ChatRead(ChatBase):
    id: UUID4

class MessagesBase(BaseModel):
    message: str
    sender_id: uuid.UUID
    chat_id: uuid.UUID

class MessagesCreate(MessagesBase):
    send_at: datetime

class MessagesRead(MessagesBase):
    id: UUID4
    


