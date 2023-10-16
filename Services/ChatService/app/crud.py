import uuid
from sqlalchemy.orm import Session
from .models import ChatRoom,Message
from .schemas import MessageRead,MessageCreate,MessageBase,ChatRead,ChatCreate,ChatBase



def create_chat(db: Session, chat: ChatCreate) -> ChatCreate:
    '''
    Создает новый чат
    '''
    db_chat = ChatRoom(
        id = uuid.uuid4(),
        buyer_id = chat.buyer_id,
        seller_id = chat.seller_id,
    )

    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def create_message(db: Session,message: MessageCreate )-> MessageCreate:
    '''
    Создает сообщение
    '''
    db_message = Message(
        id = uuid.uuid4(),
        sender_id = message.sender_id,
        chat_id = message.chat_id,
        text = message.text
    )

    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(MessageID: uuid.UUID, db: Session) -> MessageRead:
    '''
    Возвращает сообщение
    ''' 
    return db.query(Message).filter(Message.id == MessageID).first()

def get_chat(ChatID: uuid.UUID, db: Session) -> ChatRead:
    '''
    Возвращает участников чата
    ''' 
    return db.query(ChatRoom).filter(ChatRoom.id == ChatID).first()


