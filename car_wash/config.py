from urllib.parse import ParseResult, urlparse, urlunparse

from pydantic import HttpUrl, PostgresDsn, model_validator
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
    in_docker: bool = True

    filling_db: bool = True

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @model_validator(mode='after')
    def validate_not_in_docker(self) -> 'Config':
        if not self.in_docker:
            url_str = str(self.database_url)

            parsed_url: ParseResult = urlparse(url_str)
            new_netloc = 'pguser:pgpass@localhost:5434'
            updated_url = parsed_url._replace(netloc=new_netloc)

            self.database_url = PostgresDsn(urlunparse(updated_url))

        return self


config = Config()
