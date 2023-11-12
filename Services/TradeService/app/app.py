from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, RedirectResponse,HTMLResponse
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from .schemas import TradeBase,Trade,TradeCreate,TradeDelete,TradeUpdate,TradeUpdateAdmin,TradeRead,TradeAccept
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
async def get_all_trades(db: Session = Depends(get_db),skip: int = 0,limit: int = 100) -> typing.List[TradeRead] :
    return crud.get_all_trades(db, skip, limit)

@app.get("/trades/{TradeId}", summary='Возвращает информацию о сделке')
async def get_trades_info(TradeId: uuid.UUID, db: Session = Depends(get_db)) -> TradeRead :
    trade = crud.get_trade(TradeId,db)
    if trade != None:
        return trade
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.patch("/trades/{TradeId}", summary='Обновляет информацию о сделке')
async def update_trade(TradeId: uuid.UUID, trade: TradeUpdate,db: Session = Depends(get_db)) -> TradeRead :

    trade = crud.update_trade(TradeId, trade, db)
    if trade != None:
        return trade
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.patch("/trades/{TradeId}/accept", summary='Принять сделку')
async def accept_trade(TradeId: uuid.UUID, trade: TradeAccept,db: Session = Depends(get_db)) -> TradeRead :

    trade = crud.accept_trade(TradeId, trade, db)
    if trade != None:
        return trade
    return JSONResponse(status_code=404, content={"message": "Item not found"})
@app.put("/trades/{TradeId}", summary='Обновляет информацию сделки для админа')
async def update_trade_admin(TradeId: uuid.UUID, trade: TradeUpdateAdmin,db: Session = Depends(get_db)) -> TradeUpdateAdmin :

    trade = crud.update_trade_admin(TradeId, trade, db)
    if trade != None:
        return trade
    return JSONResponse(status_code=404, content={"message": "Item not found"})
@app.delete("/trades/{TradeId}", summary='Удаляет сделку из базы')
async def delete_trade(TradeId: uuid.UUID, db: Session = Depends(get_db)) -> TradeDelete :
    if crud.delete_trade(TradeId, db):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.get("/point_in_range",tags=["Geo func"], summary='Возвращает информацию о сдлках в радиусе')
async def get_spots_radius(lat: float, lon: float,radius: float,db:Session = Depends(get_db)):
    points = crud.point_in_range(lat=lat,lon=lon,radius=radius,db=db)

    if points !=None:
        return points
    return JSONResponse(status_code=404, content={"message":"No points found within the given radius"})
    
@app.get("/nearest",tags=["Geo func"], summary="Поиск ближайщей сделки")
async def find_nearest(lat: float, lon: float,db:Session = Depends(get_db)):
  
    nearest = crud.find_nearest(lat=lat,lon=lon,db=db)
    if nearest !=None:
        return nearest
    return JSONResponse(status_code=404, content={"message":"No points found within the given radius"})

@app.get("/visualize" ,tags=["Geo func"],summary="Отображение сделок на карте")
async def visualize_data(db: Session = Depends(get_db)):
    crud.create_map(db=db)
    return HTMLResponse(content=open("map.html").read(), status_code=200)
    # return RedirectResponse(url="/map")
# @app.get("/map",tags=["Geo func"])
# async def show_map():
#     return HTMLResponse(content=open("map.html").read(), status_code=200)