import uuid
from .models import ChatRoom,Messages
from .schemas import MessagesRead,MessagesCreate,MessagesBase,ChatRead,ChatCreate,ChatBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def create_chat(session: AsyncSession , chat: ChatCreate) -> ChatCreate:
    '''
    Создает новый чат
    '''
    db_chat = ChatRoom(
        id = uuid.uuid4(),
        buyer_id = chat.buyer_id,
        seller_id = chat.seller_id,
    )

    session.add(db_chat)
    await session.commit()
    await session.refresh(db_chat)
    return db_chat

async def create_message(session: AsyncSession,message: MessagesCreate )-> MessagesCreate:
    '''
    Создает сообщение
    '''
    db_message = Messages(
        id = uuid.uuid4(),
        sender_id = message.sender_id,
        chat_id = message.chat_id,
        message = message.message
    )

    session.add(db_message)
    await session.commit()
    await session.refresh(db_message)
    return db_message

async def get_message(MessageID: uuid.UUID, session: AsyncSession) -> MessagesRead:
    '''
    Возвращает сообщение
    ''' 
    async with session.begin():
        stmt = select(Messages).filter(Messages.id == MessageID)
        result = await session.execute(stmt)
        message = result.scalars().first()
        return message

async def get_chat(RoomID: uuid.UUID, session: AsyncSession) -> ChatRead:
    '''
    Возвращает участников чата
    ''' 
    async with session.begin():
        stmt = select(ChatRoom).filter(ChatRoom.id == RoomID)
        result = await session.execute(stmt)
        chat = result.scalars().first()
        return chat


