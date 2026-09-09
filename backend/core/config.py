from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_PORT : int
    DB_USER : str
    DB_NAME : str
    DB_PASSWORD : str
    DB_HOST : str
    JWT_SECRET_KEY: str | None = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REMINDER_POLL_INTERVAL_SECONDS: int = 30

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"

settings = Settings()