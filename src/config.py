import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings,SettingsConfigDict
load_dotenv()
BASE_DIR = Path(__file__).parent

class DbSettings(BaseSettings):
    url: str = "postgresql+asyncpg://postgres:postgres@localhost:5433/lazerdigital"


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str
    access_token_expire_minutes: int = 1
    refresh_token_expire_days: int = 1


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()



settings = Settings()
