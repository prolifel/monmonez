from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    APP_USER: str = ""
    model_config = SettingsConfigDict(env_file=".env")
