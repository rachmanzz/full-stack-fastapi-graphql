import graphene
from datetime import timedelta

from fastapi import HTTPException

from app.models import graphene_models
from app.crud import crud
from app.core.config import settings
from app.core import security
from app.core.security import verify_password


class Query(graphene.ObjectType):
    users = graphene.List(graphene_models.User)

    def resolve_users(parent, info, skip: int = 0, limit:int = 100):
        return crud.get_users(skip=skip, limit=limit)


class UserCreate(graphene.Mutation):
    class Arguments:
        user = graphene_models.UserCreate(required=True)

    Output = graphene_models.Success

    @staticmethod
    async def mutate(parent, info, user):
        fetched_user = await crud.get_user_by_email(email=user["email"])
        if fetched_user:
            raise HTTPException(status_code=409, detail="Email already registered")

        id = await crud.create_user(user=user)
        return {"id":id, "success": id != None}


class ItemCreate(graphene.Mutation):
    class Arguments:
        item = graphene_models.ItemCreate(required=True)

    Output = graphene_models.Success

    @staticmethod
    async def mutate(parent, info, item):
        current_user = info.context["request"].state.current_user
        id = await crud.create_user_item(item, current_user["id"])
        return {"id":id, "success": id != None}


class AuthUser(graphene.Mutation):
    class Arguments:
        user = graphene_models.UserCreate(required=True)

    Output = graphene_models.Token

    @staticmethod
    async def mutate(root, info, user) -> graphene_models.Token:

        fetched_user = await crud.get_user_by_email(email=user["email"])
        if not fetched_user:
            raise HTTPException(status_code=404, detail="Email not found")
        
        password = user["password"]
        hashed_password = fetched_user["hashed_password"]
        is_authenticated = verify_password(password, hashed_password)

        if not is_authenticated:
            raise HTTPException(status_code=401, detail="Invalid password")

        access_token_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        token = security.create_access_token(fetched_user["id"], expires_delta=access_token_expires)
        return graphene_models.Token(token, token_type="bearer")


class Mutation(graphene.ObjectType):
    user_create = UserCreate.Field()
    auth_user = AuthUser.Field()
    item_create = ItemCreate.Field()


