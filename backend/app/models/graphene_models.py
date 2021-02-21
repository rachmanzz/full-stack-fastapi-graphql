from typing import List, Optional
import graphene
import uuid


class ItemBase(graphene.ObjectType):
    title = graphene.String()
    description = graphene.String()


class ItemCreate(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class Item(ItemBase):
    id =  graphene.Int()
    owner_id = graphene.Int()


class UserBase(graphene.ObjectType):
    email = graphene.String()


class UserCreate(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class User(UserBase):
    id = graphene.Int()
    items = graphene.List(Item)


class Token(graphene.ObjectType):
    access_token = graphene.String()
    token_type = graphene.String()


class Success(graphene.ObjectType):
    id = graphene.String()
    success = graphene.Boolean()

