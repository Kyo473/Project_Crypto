from fastapi.responses import JSONResponse,HTMLResponse
from app.chat.schemas import MessagesRead,MessagesCreate,MessagesBase,ChatRead,ChatCreate,ChatBase
from app.chat import crud
import uuid
import logging
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends,Request
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.chat.models import ChatRoom,Messages,get_async_session
from app import chat,config
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

templates = Jinja2Templates(directory="app/templates")
app_config: config.Config = config.load_config()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешите запросы с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешите все HTTP-методы
    allow_headers=["*"],  # Разрешите все заголовки
)

room_managers = {}
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str,RoomID: uuid.UUID, client_id: uuid.UUID, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_database(message,RoomID,client_id)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str,RoomID: uuid.UUID, client_id: uuid.UUID):
        async for async_session in get_async_session():
            stmt = insert(Messages).values(
                message=message, chat_id=RoomID,
                sender_id=client_id
            )
            await async_session.execute(stmt)
            await async_session.commit()


manager = ConnectionManager()

@app.get("/last_messages/{RoomID}",tags=["ChatRoom"])
async def get_last_messages(RoomID: uuid.UUID, session: AsyncSession = Depends(get_async_session)) -> List[MessagesRead]:
    query = (
        select(Messages)
        .filter(Messages.chat_id == RoomID)  
        .order_by(Messages.send_at.desc())  
        .limit(20)
    )
    messages = await session.execute(query)
    return messages.scalars().all()



@app.websocket("/ws/{RoomID}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, RoomID: uuid.UUID, client_id: uuid.UUID):
    # Создайте или получите ConnectionManager для данной комнаты
    if RoomID not in room_managers:
        room_managers[RoomID] = ConnectionManager()

    manager = room_managers[RoomID]

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} in Room {RoomID} says: {data}",RoomID,client_id,add_to_db=True)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left Room:{RoomID}",RoomID,client_id,add_to_db=False)

@app.get("/chat",tags=["ChatRoom"])
def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "hostportDns": app_config.hostportDns})


@app.post("/chatroom",tags=["ChatRoom"], status_code=201, response_model=ChatRead,summary='Создает чат')
async def create_chat(chat: ChatCreate, session: AsyncSession  = Depends(get_async_session)) -> ChatRead :
    return await crud.create_chat(session=session, chat=chat)

@app.get("/chatroom/{RoomID}",tags=["ChatRoom"], summary='Возвращает информацию о чате')
async def get_chat(RoomID: uuid.UUID, session: AsyncSession  = Depends(get_async_session)) -> ChatRead :
    chat = await crud.get_chat(RoomID,session)
    if chat != None:
        return chat
    return await JSONResponse(status_code=404, content={"ChatRoom:": "Item not found"})

@app.on_event("startup")
async def on_startup():
    await chat.database.initializer.init_database(
        app_config.postgres_dsn.unicode_string())