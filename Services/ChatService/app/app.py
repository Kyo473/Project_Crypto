from fastapi import FastAPI, Depends
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from .schemas import MessageRead,MessageCreate,MessageBase,ChatRead,ChatCreate,ChatBase
from . import crud
from . import config
import uuid
from typing import Dict, List
from fastapi.logger import logger

cfg: config.Config = config.load_config()

# init database
logger.info('Initializing database...')
SessionLocal = DB_INITIALIZER.init_database(str(cfg.postgres_dsn))

# init app
app = FastAPI(
    version='0.0.2',
    title='Chat Management Service'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/message", status_code=201, tags=["Message"], response_model=MessageCreate, summary='Добавляет сообщение в базу')
async def create_message(message: MessageCreate, db: Session = Depends(get_db)) -> MessageCreate:
    return crud.create_message(db=db, message=message)
   

@app.get("/message/{MessageID}",tags=["Message"], summary='Возвращает сообщение')
async def get_message(MessageID: uuid.UUID, db: Session = Depends(get_db)) -> MessageRead :
    message = crud.get_message(MessageID,db)
    if message != None:
        return message
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.post("/chat",tags=["Chat"], status_code=201, response_model=ChatCreate,summary='Создает чат')
async def create_chat(chat: ChatCreate, db: Session = Depends(get_db)) -> ChatCreate :
    return crud.create_chat(db=db, chat=chat)

@app.get("/chat/{ChatID}",tags=["Chat"], summary='Возвращает информацию о чате')
async def get_chat(ChatID: uuid.UUID, db: Session = Depends(get_db)) -> ChatRead :
    chat = crud.get_chat(ChatID,db)
    if chat != None:
        return chat
    return JSONResponse(status_code=404, content={"Chat:": "Item not found"})
