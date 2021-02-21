from typing import Generator, Optional

from fastapi import Depends, Request, FastAPI, HTTPException, status
from fastapi.security import utils, OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import jwt
from fastapi import FastAPI, Header

from app.core.config import settings
from app.core import security
from app.crud import crud
from app.models import graphene_models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(request: Request) -> Optional[graphene_models.User]:
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        return None

    _, token = utils.get_authorization_scheme_param(authorization)
    return await crud.get_current_user(token=token)
