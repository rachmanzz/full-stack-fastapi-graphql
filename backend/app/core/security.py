from jose import jwt
from passlib.context import CryptContext
from typing import Any, Union
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException

import time

from app.core.config import settings
from app.models import graphene_models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
        )
    to_encode = {
        "exp": expire.timestamp(), 
        "sub": str(subject),
        "iat": datetime.utcnow()}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        date_time_obj = datetime.fromtimestamp(payload["exp"])
        if date_time_obj < datetime.utcnow():
            raise HTTPException(status_code=403, detail="Token expired")

        return int(payload["sub"])
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
