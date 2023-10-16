from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.chat.schemas import MessagesRead,MessagesCreate,MessagesBase,ChatRead,ChatCreate,ChatBase
from app.chat import crud
import uuid
import logging
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends,APIRouter,Request
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.chat.models import ChatRoom,Messages,get_async_session
from app import chat,config
# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

app_config: config.Config = config.load_config()
app = FastAPI()
room_managers = {}
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str):
        async with get_async_session() as async_session:
            stmt = insert(Messages).values(
                message=message
            )
            await async_session.execute(stmt)
            await async_session.commit()


manager = ConnectionManager()

@app.get("/last_messages")
async def get_last_messages(session: AsyncSession = Depends(get_async_session),) -> List[MessagesRead]:
    query = select(Messages).order_by(Messages.id.desc()).limit(20)
    messages = await session.execute(query)
    return messages.scalars().all()



@app.websocket("/ws/{RoomID}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, RoomID: uuid.UUID, client_id: int):
    # Создайте или получите ConnectionManager для данной комнаты
    if RoomID not in room_managers:
        room_managers[RoomID] = ConnectionManager()

    manager = room_managers[RoomID]

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} in Room {RoomID} says: {data}", add_to_db=False)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} in Room {RoomID} left the chat", add_to_db=False)



@app.post("/message", status_code=201, tags=["Message"], response_model=MessagesCreate, summary='Добавляет сообщение в базу')
async def create_message(message: MessagesCreate, session: AsyncSession  = Depends(get_async_session)) -> MessagesCreate:
    return await crud.create_message(session=session, message=message)
   

@app.get("/message/{MessageID}",tags=["Message"], summary='Возвращает сообщение')
async def get_message(MessageID: uuid.UUID, session: AsyncSession  = Depends(get_async_session)) -> MessagesRead :
    message = crud.get_message(MessageID,session)
    if message != None:
        return message
    return await JSONResponse(status_code=404, content={"message": "Item not found"})

@app.post("/chatroom",tags=["ChatRoom"], status_code=201, response_model=ChatCreate,summary='Создает чат')
async def create_chat(chat: ChatCreate, session: AsyncSession  = Depends(get_async_session)) -> ChatCreate :
    return await crud.create_chat(session=session, chat=chat)

@app.get("/chatroom/{RoomID}",tags=["ChatRoom"], summary='Возвращает информацию о чате')
async def get_chat(RoomID: uuid.UUID, session: AsyncSession  = Depends(get_async_session)) -> ChatRead :
    chat = crud.get_chat(RoomID,session)
    if chat != None:
        return chat
    return await JSONResponse(status_code=404, content={"ChatRoom:": "Item not found"})

@app.on_event("startup")
async def on_startup():
    await chat.database.initializer.init_database(
        app_config.postgres_dsn.unicode_string())