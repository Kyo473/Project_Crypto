from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from .schemas import TradeBase,Trade,TradeCreate,TradeDelete,TradeUpdate
from . import crud
from . import config
import typing
import uuid
from fastapi.logger import logger

cfg: config.Config = config.load_config()

# init database
logger.info('Initializing database...')
SessionLocal = DB_INITIALIZER.init_database(str(cfg.postgres_dsn))

# init app
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


@app.post("/trade", status_code=201, response_model=Trade,summary='Добавляет сделку в базу')
async def create_trade(trade: TradeCreate, db: Session = Depends(get_db)) -> Trade :
    return crud.create_trade(db=db, trade=trade)

@app.get("/trades",summary='Возвращает список сделок',response_model=list[Trade])
async def get_all_trades(db: Session = Depends(get_db),skip: int = 0,limit: int = 100) -> typing.List[Trade] :
    return crud.get_all_trades(db, skip, limit)

@app.get("/trades/{TradeId}", summary='Возвращает информацию о сделке')
async def get_trades_info(TradeId: uuid.UUID, db: Session = Depends(get_db)) -> Trade :
    trade = crud.get_trade(TradeId,db)
    if trade != None:
        return trade
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.put("/trades/{TradeId}", summary='Обновляет информацию о сделке')
async def update_trade(TradeId: uuid.UUID, trade: TradeUpdate,db: Session = Depends(get_db)) -> TradeUpdate :

    trade = crud.update_trade(TradeId, trade, db)
    if trade != None:
        return trade
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.delete("/trades/{TradeId}", summary='Удаляет сделку из базы')
async def delete_trade(TradeId: uuid.UUID, db: Session = Depends(get_db)) -> TradeDelete :
    if crud.delete_trade(TradeId, db):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})

