import logging
from fastapi import FastAPI
from . import config,users

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

app_config: config.Config = config.load_config()

app = FastAPI(
    version='0.0.1',
    title='User Management Service'
)

users.inject_secrets(
    jwt_secret=app_config.jwt_secret.get_secret_value(),
    verification_token_secret=app_config.verification_token_secret.get_secret_value(),
    reset_password_token_secret=app_config.reset_password_token_secret.get_secret_value()
)
users.include_routers(app)

@app.on_event("startup")
async def on_startup():
    await users.database.initializer.init_database(
        app_config.postgres_dsn.unicode_string()
    )