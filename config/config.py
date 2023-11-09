from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    REDIS_HOST: str
    REDIS_PORT: int
    ACCESS_TOKEN_TTL: int
    REFRESH_TOKEN_TTL: int

    MONGO_HOST: str
    MONGO_PORT: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

    ELASTIC_HOST: str
    ELASTIC_PORT: int

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    QUEUE_NAME_LIST: List

    PODCAST_USER_BOOKMARKED_CHANNEL_URL: str

    ACCOUNT_GET_USER_EMAIL_URL: str
    NOTIFICATION_RSS_UPDATE_NOTIF_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


@lru_cache
def get_settings():
    return settings
