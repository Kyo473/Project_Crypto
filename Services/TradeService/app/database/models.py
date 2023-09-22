from sqlalchemy import MetaData, Column, Integer, String,Table, TIMESTAMP,JSON,ForeignKey
from datetime import datetime
from .database import Base

metadata = MetaData()

class tags(Base):
    __tablename__ = "tags"

    id = Column("id",Integer,primary_key=True)
    desciption = Column("desciption",String,default='')
    geo_tag = Column("geo_tag",JSON)



class trades(Base):
    __tablename__ = "trades"

    id = Column("id",Integer, primary_key=True)
    buyer_id = Column("buyer_id",Integer)
    seller_id = Column("seller_id",Integer)
    price = Column("price",Integer, nullable=False)
    currency = Column("currency",String, nullable=False)
    description = Column("description",String,default='')
    created_at = Column("created_at",TIMESTAMP, default=datetime.utcnow)
    geo_tag_id = Column("geo_tag_id",Integer,ForeignKey("tags.id"))
    hide = Column("hide",String)
