from sqlalchemy import Column, String,TIMESTAMP,Float,UUID,ForeignKey
from . import database
from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

class ChatRoom(database.BASE):
    __tablename__ = 'chats'
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    seller_id = Column(UUID) 
    buyer_id = Column(UUID) 
    
class Messages(database.BASE):
    __tablename__ = 'messages'
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    send_at = Column(TIMESTAMP, default=datetime.utcnow)
    message = Column(String)
    sender_id = Column(UUID, primary_key=True)
    chat_id = Column(UUID)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.initializer.async_session_maker() as session:
        yield session
