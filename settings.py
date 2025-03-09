from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PG_USER: str
    PG_PASSWORD: str 
    PG_DATABASE: str
    PG_HOSTNAME: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )


STAGE=os.environ.get("STAGE")
if STAGE == "nprod":
    settings = Settings()
elif STAGE == "prod":
    settings = Settings(_env_file="prod.env")