from sqlalchemy import Column, Integer, String,TIMESTAMP,Float,UUID
from datetime import datetime
from ..database import Base
from geoalchemy2 import Geometry
import uuid

class trades(Base):
    __tablename__ = "trades"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    buyer_id = Column(UUID) 
    seller_id = Column(UUID) 
    buyer_address = Column(String, default='')
    seller_address = Column(String,default='')
    price = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    description = Column(String, default='')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    lat = Column(Float)
    lon = Column(Float)
    geo_tag = Column(Geometry('POINT', srid=4326))
    hide = Column(String, default='Create')
    
