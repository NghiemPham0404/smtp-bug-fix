from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import List, Optional
from pydantic_settings import BaseSettings


class MailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: Optional[int] = 587
    MAIL_SERVER: Optional[str] = "smtp.gmail.com"
    MAIL_FROM_NAME: Optional[str] = "Footprints support"
    MAIL_STARTTLS: Optional[bool] = True    # ✅ replaces MAIL_TLS
    MAIL_SSL_TLS: Optional[bool] = False
    USE_CREDENTIALS: Optional[bool] = True
    VALIDATE_CERTS: Optional[bool] = True

    class Config:
        env_file = ".env"

settings = MailSettings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
)

fm = FastMail(conf)

# Setup Jinja2 Environment
templates = Environment(
    loader=FileSystemLoader("/app/templates"),
    autoescape=select_autoescape(["html", "xml"])
)
