from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env')

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    DOWNLOAD_DIRECTORY: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return str(MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ))


settings = Settings()
