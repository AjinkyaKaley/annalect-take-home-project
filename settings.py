from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PG_USER: str
    PG_PASSWORD: str 
    PG_DATABASE: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

settings = Settings()