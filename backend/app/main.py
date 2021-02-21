import fastapi
import uvicorn
import sys

from fastapi import FastAPI, Request, Depends
from starlette.graphql import GraphQLApp
from starlette.datastructures import URL
from graphql.execution.executors.asyncio import AsyncioExecutor
from fastapi.middleware.cors import CORSMiddleware
import graphene

from sqlalchemy.orm import Session

from app.api import deps
from app.api import gql
from app.db.database import database
from app.models import graphene_models


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


schema = graphene.Schema(
    query=gql.Query,
    mutation=gql.Mutation)

graphql_app = GraphQLApp(
    schema=schema,
    executor_class=AsyncioExecutor)


@app.get('/')
async def graphiql(request: Request, current_user: graphene_models.User = Depends(deps.get_current_user)):
    request._url = URL('/gql')
    return await graphql_app.handle_graphiql(request=request)


@app.post('/gql')
async def graphql(request: Request, current_user: graphene_models.User = Depends(deps.get_current_user)):
    request.state.current_user = current_user
    return await graphql_app.handle_graphql(request=request)


if __name__ == '__main__':
    uvicorn.run(app)
