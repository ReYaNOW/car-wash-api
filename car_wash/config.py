from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn
    secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    debug: bool = False
    filling_db: bool = False

    model_config = SettingsConfigDict(env_file='.env')


config = Config()
