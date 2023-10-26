import logging

from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

class Config(BaseSettings):
    postgres_dsn: PostgresDsn = Field(
        default='postgresql://user:pass@localhost:5432/foobar',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )

    jwt_secret: SecretStr = Field(
        default='jwt_secret',
        env='JWT_SECRET',
        alias='JWT_SECRET'
    )

    reset_password_token_secret: SecretStr = Field(
        default='reset_password_token_secret',
        env='RESET_PASSWORD_TOKEN_SECRET',
        alias='RESET_PASSWORD_TOKEN_SECRET'
    )

    verification_token_secret: SecretStr = Field(
        default='verification_token_secret',
        env='VERIFICATION_TOKEN_SECRET',
        alias='VERIFICATION_TOKEN_SECRET'
    )

    class Config:
        env_file = ".env"
        extra = 'allow'


def load_config() -> Config:
    app_config: Config = Config()
    logger.info(
        'Service configuration loaded:\n' +
        f'{app_config.model_dump_json(by_alias=True, indent=4)}'
    )
    return app_config
    