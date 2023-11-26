import aio_pika
import asyncio
import smtplib
from email.message import EmailMessage
from pydantic import Field
from pydantic_settings import BaseSettings
import logging
import re
class Config(BaseSettings):
    email: str = Field(
        default='',
        env='SMTP_EMAIL',
        alias='SMTP_EMAIL'
    )
    password: str = Field(
        default='',
        env='SMTP_PASS',
        alias='SMTP_PASS'
    )
    smtp_url: str = Field(
        default='smtp.mail.ru',
        env='SMTP_URL',
        alias='SMTP_URL'
    )
    smtp_port:str = Field(
        default='465',
        env='SMTP_PORT',
        alias='SMTP_PORT'
    )
    amqp_url: str = Field(
        default='amqp://guest:guest@localhost/',
        env='AMQP',
        alias='AMQP'
    )

    class Config:
        env_file = ".env"


def load_config() -> Config:
    return Config()


cfg: Config = load_config()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("email_logs.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info(f"Email:{cfg.email}")
logger.info(f"Pass:{cfg.password}")
logger.info(f"Url:{cfg.smtp_url}")
logger.info(f"Port:{cfg.smtp_port}")
async def consume_from_queue():
    connection = await aio_pika.connect_robust(cfg.amqp_url)
    channel = await connection.channel()
    queue = await channel.declare_queue("email_queue")
    
    async def extract_email_address(message_body):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, message_body)
        if match:
            return match.group(0)
        return None
    
    async def send_email(message_body):
        email_address = await extract_email_address(message_body)
        logger.info(email_address)
        msg = EmailMessage()
        msg.set_content("Вы успешно зарегистрировались на платформе")
        msg['Subject'] = 'Сообщение о успешной регистрации'
        msg['From'] = cfg.email
        msg['To'] = email_address

        try:
            with smtplib.SMTP_SSL(f'{cfg.smtp_url}', cfg.smtp_port) as smtp:
                smtp.login(f"{cfg.email}", f"{cfg.password}")
                smtp.send_message(msg)
                logger.info("Email успешно отправлен!")
        except Exception as e:
            logger.error(f"Ошибка при отправке email: {e}")

    async def callback(message):
        async with message.process():
            email_body = message.body.decode('utf-8')
            await send_email(email_body)

    await queue.consume(callback)

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(consume_from_queue())
    loop.run_forever()
