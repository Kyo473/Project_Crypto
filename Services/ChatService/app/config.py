from pydantic import PostgresDsn,Field,AnyUrl
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    postgres_dsn: PostgresDsn = Field(
        default='postgresql+asyncpg://user:pass@localhost:5432/foobar',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )
    hostportDns: AnyUrl = Field(
        default='localhost:5001',
        env='HOSTPORTDNS_WS',
        alias='HOSTPORTDNS_WS'
    )
    class Config:
        env_file = ".env"


def load_config() -> Config:
    return Config()