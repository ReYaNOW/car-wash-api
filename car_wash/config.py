from pydantic import HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn
    secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    admin_username: str
    admin_password: str

    s3_server_url: HttpUrl
    use_ssl: bool
    s3_access_key: str
    s3_secret_access_key: str
    default_bucket: str = 'default-bucket'

    debug: bool = False

    filling_db: bool = False

    model_config = SettingsConfigDict(env_file='.env')


config = Config()
