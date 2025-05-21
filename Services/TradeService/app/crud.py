import typing
import uuid
from sqlalchemy.orm import Session
from .models import trades
from .schemas import Trade,TradeCreate,TradeDelete,TradeUpdate,TradeUpdateAdmin,TradeRead,TradeAccept
from shapely.geometry import Point
from geoalchemy2 import functions as geofunc
from geoalchemy2 import WKTElement
import folium
from geoalchemy2.shape import to_shape
from datetime import datetime 
def create_trade(db: Session, trade: TradeCreate) -> TradeCreate:
    '''
    Создает новое объявление сделки в БД
    '''
    shapely_point = Point(trade.lat, trade.lon)
    geo_point = WKTElement(shapely_point.wkt, srid=4326)
    db_trade = trades(
        id = uuid.uuid4(),
        seller_id = trade.seller_id,\
        seller_address = trade.seller_address,
        price = trade.price,
        amount =trade.amount,
        currency = trade.currency,
        created_at = datetime.utcnow(),
        description = trade.description,
        hide  = trade.hide,
        lat = trade.lat,
        lon = trade.lon,
        geo_tag = geo_point
    )

    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_all_trades(db: Session,trade: TradeRead, skip: int = 0, limit: int = 100) -> typing.List[TradeRead]:
    '''
    Возвращает инфомрмацию о всех сделках 
    '''
    return db.query(trades).all()

def get_trade(TradeId: uuid.UUID, db: Session) -> TradeRead:
    '''
    Возвращает инфомрмацию о сделке
    ''' 
    return db.query(trades).filter(trades.id == TradeId).first()

def update_trade( TradeId: uuid.UUID, trade: TradeUpdate ,db: Session) -> TradeUpdate:
    '''
    Обновляет информацию о сделке
    '''
    result =    db.query(trades).filter(trades.id == TradeId).update(trade.dict())
    db.commit()

    if result == 1:
        return get_trade(TradeId, db)
    return None

def accept_trade( TradeId: uuid.UUID, trade: TradeAccept ,db: Session) -> TradeRead:
    '''
    Обновляет информацию о сделке
    '''
    result =    db.query(trades).filter(trades.id == TradeId).update(trade.dict())
    db.commit()

    if result == 1:
        return get_trade(TradeId, db)
    return None
def update_trade_admin( TradeId: uuid.UUID, trade: TradeUpdateAdmin ,db: Session) -> TradeUpdateAdmin:
    '''
    Обновляет информацию о сделке
    '''
    result =    db.query(trades).filter(trades.id == TradeId).update(trade.dict())
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

def point_in_range(lat: float, lon: float, radius: float,db:Session):
    """
    Отдает список меток в определенном радиусе
    """
    shapely_point = Point(lon, lat)
    wkt_point = WKTElement(shapely_point.wkt, srid=4326)
    points = db.query(trades).filter(trades.geo_tag.distance_centroid(wkt_point) <= radius).all()
    result = []
    for point in points:
        shapely_point = to_shape(point.geo_tag)
        result.append({"id_trade":point.id, "latitude": shapely_point.x, "longitude": shapely_point.y})
    if result != []:
        return result
    
def find_nearest(lat: float, lon: float,db:Session):
    """
    Ищет самую ближнюю точку  
    """
    shapely_point = Point(lon, lat)
    wkt_point = WKTElement(shapely_point.wkt, srid=4326)
    nearest = db.query(trades)\
        .order_by(geofunc.ST_Distance(trades.geo_tag, wkt_point))\
        .first()
    
    shapely_point = to_shape(nearest.geo_tag)
    result = {"id_trade":nearest.id, "latitude": shapely_point.x, "longitude": shapely_point.y}
    return result

def create_map(db:Session):
    """
    Отображает метки на карте
    """
    geo_data = db.query(trades).all()
    map = folium.Map(location=[0, 0], zoom_start=2)

    for point in geo_data:
        shapely_point = to_shape(point.geo_tag)
        latitude = shapely_point.x
        longitude = shapely_point.y
        folium.Marker([latitude, longitude]).add_to(map)
    map.save("map.html")
    return map