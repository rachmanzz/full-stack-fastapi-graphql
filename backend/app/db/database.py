from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import settings

database = databases.Database(
    settings.SQLALCHEMY_DATABASE_URI, 
    ssl=settings.SQLALCHEMY_DATABASE_SSL, 
    min_size=settings.SQLALCHEMY_DATABASE_MIN_POOL, 
    max_size=settings.SQLALCHEMY_DATABASE_MAX_POOL
)