from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn
    debug: bool = False

    model_config = SettingsConfigDict(env_file='.env')


config = Config()
