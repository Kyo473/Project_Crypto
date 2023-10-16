from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base , DeclarativeMeta
from sqlalchemy.orm import sessionmaker

class DatabaseInitializer():
    def __init__(self, base) -> None:
        self.base = base

    def init_database(self, postgres_dsn):
        self.engine = create_engine(postgres_dsn)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)

        self.base.metadata.create_all(bind=self.engine)
        return self.SessionLocal

Base: DeclarativeMeta = declarative_base()
DB_INITIALIZER = DatabaseInitializer(Base)
