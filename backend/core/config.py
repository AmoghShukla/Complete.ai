from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_PORT : int
    DB_USER : str
    DB_NAME : str
    DB_PASSWORD : str
    DB_HOST : str

settings = Settings()