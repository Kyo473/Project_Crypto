from pydantic import PostgresDsn,Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    postgres_dsn: PostgresDsn = Field(
        default='postgresql://user:pass@localhost:5432/foobar',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )
    class Config:
        env_file = ".env"


def load_config() -> Config:
    return Config()