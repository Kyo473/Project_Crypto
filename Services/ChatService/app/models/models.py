from sqlalchemy import Column, String,TIMESTAMP,Float,UUID,ForeignKey
from ..database import Base
from datetime import datetime
import uuid

class ChatRoom(Base):
    __tablename__ = 'chats'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    seller_id = Column(UUID) 
    buyer_id = Column(UUID) 
    
class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    text = Column(String)
    send_at = Column(TIMESTAMP, default=datetime.utcnow)
    sender_id = Column(UUID, primary_key=True)
    chat_id = Column(UUID, ForeignKey('chats.id'))

