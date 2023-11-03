import logging

from pydantic import Field, FilePath, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

class Config(BaseSettings):
    jwt_secret: SecretStr = Field(
        default='jwt_secret',
        env='JWT_SECRET',
        alias='JWT_SECRET'
    )

    policies_config_path: FilePath = Field(
        default='policies.yaml',
        env='POLICIES_CONFIG_PATH',
        alias='POLICIES_CONFIG_PATH'
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
    