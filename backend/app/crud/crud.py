from enum import Enum

from sqlalchemy.orm import Session
from fastapi import HTTPException

from typing import Any, Dict, List, Optional, Union
from graphql import GraphQLError

from app.core.security import get_password_hash, verify_password
from app.models import sql_models, graphene_models
from app.core import security
from app.db.database import database


async def get_user(id: int) -> Optional[Dict]:
    query = sql_models.users.select().where(sql_models.users.c.id == int(id))
    user = await database.fetch_one(query=query)
    return dict(user) if user else None


async def get_user_by_email(email: str) -> Optional[Dict]:
    query = sql_models.users.select().where(sql_models.users.c.email == email)
    user = await database.fetch_one(query=query)
    return dict(user) if user else None


async def get_users(skip: int = 0, limit: int = 100) -> Optional[List]:
    query = sql_models.users.select(offset=skip, limit=limit)
    users = await database.fetch_all(query=query)
    users = [dict(user) for user in users] if users else None
    return users


async def create_user(user: graphene_models.UserCreate) -> int:
    params = dict(user)
    params["hashed_password"] = security.get_password_hash(user["password"])
    del params["password"]
    query = sql_models.users.insert().values(**params)
    return await database.execute(query)


async def get_current_user(token: str) -> Optional[graphene_models.User]:
    user_id = security.decode_access_token(token)
    fetched_user = await get_user(id=user_id)
    if not fetched_user:
        raise HTTPException(status_code=404, detail="User not found")
    return fetched_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(sql_models.Item).offset(skip).limit(limit).all()


async def create_user_item(item: graphene_models.ItemCreate, user_id: int) -> int:
    params = dict(item)
    params["owner_id"] = user_id
    query = sql_models.items.insert()
    return await database.execute(query=query, values=params)
