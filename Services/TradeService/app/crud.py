import typing
from sqlalchemy.orm import Session
from .database import models
from . import schemas

def create_trade(
        db: Session, trade: schemas.TradeCreate
    ) -> models.trades:
    '''
    Создает новое объявление сделки в БД
    '''
    db_trade = models.trades(
        price = trade.price,
        currency = trade.currency,
        description = trade.description
    )

    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_trades(
        db: Session, skip: int = 0, limit: int = 100
    ) -> typing.List[models.trades]:
    '''
    Возвращает инфомрмацию о всех сделках 
    '''
    return  db.query(models.trades) \
            .offset(skip) \
            .limit(limit) \
            .all()

def get_trade(
        db: Session, trade_id: int
    ) -> models.trades:
    '''
    Возвращает информацию о конкретной сделке
    '''
    return  db.query(models.trades) \
            .filter(models.trades.id == trade_id) \
            .first()

def update_trade(
        db: Session, trade_id: int, trade: schemas.TradeCreate
    ) -> models.trades:
    '''
    Обновляет информацию о сделке
    '''
    result =    db.query(models.trades) \
                .filter(models.trades.id == trade_id) \
                .update(trade.dict())
    db.commit()

    if result == 1:
        return get_trade(db, trade_id)
    return None


def delete_trade(
        db: Session, trade_id: int
    ) -> bool:
    '''
    Удаляет информацию о сделке
    '''
    result =    db.query(models.trades) \
                .filter(models.trades.id == trade_id) \
                .delete()
    db.commit()
    return result == 1