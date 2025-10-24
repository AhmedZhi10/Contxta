from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings for the current stage.
    We only need Redis for Celery right now.
    """
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    DATABASE_URL: str
    REDIS_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')


# This creates the settings object, which now only expects REDIS_URL.
settings = Settings()