from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@db/fastapi"
    SQLALCHEMY_DATABASE_SSL = False
    SQLALCHEMY_DATABASE_MIN_POOL = 1
    SQLALCHEMY_DATABASE_MAX_POOL = 20

settings = Settings()
