from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase


class DatabaseInitializer():
    def __init__(self, base: DeclarativeBase) -> None:
        self.__base: DeclarativeBase = base
        self.__async_session_maker = None

    async def init_database(self, postgres_dsn):
        engine = create_async_engine(postgres_dsn)
        self.__async_session_maker = async_sessionmaker(
            engine, expire_on_commit=False
        )
        async with engine.begin() as conn:
            await conn.run_sync(self.__base.metadata.create_all)

    @property
    def async_session_maker(self):
        return self.__async_session_maker

BASE = declarative_base()
initializer = DatabaseInitializer(BASE)