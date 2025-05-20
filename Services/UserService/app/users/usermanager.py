import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from app import config
from app.users import models, secretprovider
from fastapi_users.exceptions import UserAlreadyExists, UserNotExists
import pika
cfg: config.Config = config.load_config()

def send_email_to_queue(email):
    
    params = pika.URLParameters(cfg.amqp)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=params.host,
        port=params.port,
        virtual_host=params.virtual_host,
        credentials=params.credentials
    ))
    channel = connection.channel()
    queue_name = "email_queue"

    
    channel.queue_declare(queue_name)

    channel.basic_publish(
    exchange='', routing_key='email_queue', body=email)

    connection.close()
    print(f"Email отправлен в очередь RabbitMQ: {email}")
    
class UserManager(UUIDIDMixin, BaseUserManager[models.User, uuid.UUID]):

    async def on_after_register(self, user: models.User, request=None):
        print(f"User {user.id} has registered.")
        send_email_to_queue(user.email)

    async def on_after_forgot_password(
        self, user: models.User, token: str, request=None
    ):
        print(f"User {user.id} has forgotten their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: models.User, token: str, request=None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
    
    async def create(self, user_create, safe: bool = False, **kwargs):
        try:
            # вызываем родительский метод
            return await super().create(user_create, safe=safe, **kwargs)
        except UserAlreadyExists:
            # кастомное сообщение
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь уже существует"
            )

    async def get_by_email(self, email: str):
        try:
            return await super().get_by_email(email)
        except UserNotExists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователя с такими данными не существует"
            )
async def get_user_manager(
    user_db=Depends(models.get_user_db),
    secret_provider: secretprovider.SecretProvider=Depends(secretprovider.get_secret_provider)
):
    user_manager = UserManager(user_db)
    user_manager.reset_password_token_secret = secret_provider.reset_password_token_secret
    user_manager.verification_token_secret = secret_provider.verification_token_secret
    yield user_manager
