from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from .schemas.trade import Trade,TradeCreate
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from . import crud
from .config import DB_USERS,DB_PASS,DB_HOST,DB_HOST,DB_PORT,DB_NAME
import typing
from fastapi.logger import logger


# init database
logger.info('Initializing database...')
SessionLocal = DB_INITIALIZER.init_database(f"postgresql://{DB_USERS}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

app = FastAPI(
    version='0.0.2',
    title='Trade Management Service'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/trade", status_code=201, response_model=Trade,
    summary='Добавляет сделку в базу'
)
async def create_trade(trade: TradeCreate, db: Session = Depends(get_db)) -> Trade :
    return crud.create_trade(db=db, trade=trade)

@app.get(
    "/trades",
    summary='Возвращает список сделок',
    response_model=list[Trade]
)
async def get_trades(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
    ) -> typing.List[Trade] :
    return crud.get_trades(db, skip, limit)

@app.get("/trades/{TradeId}", summary='Возвращает информацию о сделке')
async def get_device_info(
        TradeId: int, db: Session = Depends(get_db)
    ) -> Trade :
    trade = crud.get_trade(db, TradeId)
    if trade != None:
        return trade
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.put("/trades/{TradeId}", summary='Обновляет информацию о сделке')
async def update_trade(
        TradeId: int, 
        trade: TradeCreate,
        db: Session = Depends(get_db)
    ) -> Trade :

    trade = crud.update_trade(db, TradeId, trade)
    if trade != None:
        return trade
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.delete("/trades/{TradeId}", summary='Удаляет сделку из базы')
async def delete_trade(
        TradeId: int, db: Session = Depends(get_db)
    ) -> Trade :
    if crud.delete_trade(db, TradeId):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})

