# why config.py below doesn't override my settings from .env and uses defaults?
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str = 'contacts'
    query_table_name: str = 'contacts'
    query_logs_table_name: str = 'query_logs'

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')


settings = Settings()
