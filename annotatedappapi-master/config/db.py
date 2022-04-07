from pydantic import BaseSettings,PostgresDsn,validator
from typing import Any, Dict, Optional

class Settings(BaseSettings):
    mongo_username: str
    mongo_password: str
    mongo_host: str
    mongo_port: str
    class Config:
        env_file = '.env'
