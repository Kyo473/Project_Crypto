from sqlalchemy import MetaData, Column, Integer, String,Table, TIMESTAMP,JSON,ForeignKey
from datetime import datetime

metadata = MetaData()

tags= Table(
    "tags",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("Desciption",String,default=''),
    Column("geo_tag",JSON)
)


trades = Table(
    "trades",
    metadata,
    Column("id",Integer, primary_key=True),
    Column("buyer_id",Integer, primary_key=True),
    Column("seller_id",Integer, primary_key=False),
    Column("price",Integer, nullable=False),
    Column("currency",String, nullable=False),
    Column("created_at",TIMESTAMP, default=datetime.utcnow),
    Column("geo_tag_id",Integer,ForeignKey("tags.id")),
    Column("hide",String,nullable=False)
)