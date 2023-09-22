from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DatabaseInitializer():
    def __init__(self, base) -> None:
        self.base = base

    def init_database(self, postgres_dsn):
        engine = create_engine(postgres_dsn)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


        self.base.metadata.create_all(bind=engine)
        return SessionLocal

Base = declarative_base()
DB_INITIALIZER = DatabaseInitializer(Base)
