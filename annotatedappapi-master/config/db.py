from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_username: str
    mongo_password: str
    mongo_host: str
    mongo_port: str


    class Config:
        env_file = '.env'
