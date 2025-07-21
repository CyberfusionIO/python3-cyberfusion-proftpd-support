from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_path: Path

    user_expire_hours: int = 1

    class Config:
        env_prefix = "proftpd_support_"

        env_file = ".env", "/etc/proftpd-support.conf"


settings = Settings()
