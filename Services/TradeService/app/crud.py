import typing
import uuid
from sqlalchemy.orm import Session
from .models import trades
from .schemas import TradeBase,Trade,TradeCreate,TradeDelete,TradeUpdate

def create_trade(db: Session, trade: TradeCreate) -> TradeCreate:
    '''
    Создает новое объявление сделки в БД
    '''
    db_trade = trades(
        id = uuid.uuid4(),
        price = trade.price,
        currency = trade.currency,
        description = trade.description,
        lat = trade.lat,
        lon = trade.lon
    )

    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_all_trades(db: Session, skip: int = 0, limit: int = 100) -> typing.List[trades]:
    '''
    Возвращает инфомрмацию о всех сделках 
    '''
    return db.query(trades).all()

def get_trade(TradeId: uuid.UUID, db: Session) -> Trade:
    '''
    Возвращает инфомрмацию о сделке
    ''' 
    return db.query(trades).filter(trades.id == TradeId).first()

def update_trade( TradeId: uuid.UUID, trade: TradeUpdate ,db: Session) -> TradeUpdate:
    '''
    Обновляет информацию о сделке
    '''
    result =    db.query(trades) \
                .filter(trades.id == TradeId) \
                .update(trade.dict())
    db.commit()

    if result == 1:
        return get_trade(TradeId, db)
    return None


def delete_trade(TradeId: uuid.UUID,db: Session) -> TradeDelete:
    '''
    Удаляет информацию о сделке
    '''
    result =    db.query(trades) \
                .filter(trades.id == TradeId) \
                .delete()
    db.commit()
    return result == 1