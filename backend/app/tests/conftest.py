import graphene
import uvicorn
import pytest
from httpx import AsyncClient
from multiprocessing import Process
import time
import string 
import random 

from app.main import app, schema
from app.tests import test_gql
from app.db.database import database
from app.models import sql_models


# file used for postman testing
with open("schema.sdl", "w") as text_file:
    text_file.write(str(schema))


def run_server():
    uvicorn.run(app)

@pytest.fixture(scope="module")
def credentials():
    random_string = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 4)) 

    email = f"unitest_{random_string}@bar.com"
    return {
        "email":email, 
        "password":"password"
    }


@pytest.fixture(scope="module")
def server(credentials):
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start() 
    time.sleep(.5)
    yield

    # cleanup
    conn = sql_models.engine
    query = sql_models.users.select().where(sql_models.users.c.email == credentials["email"])
    user_result = next(conn.execute(query))

    query = sql_models.items.delete().where(sql_models.items.c.owner_id == user_result["id"])
    conn.execute(query)


    query = sql_models.users.delete().where(sql_models.users.c.email == credentials["email"])
    conn.execute(query)
    proc.kill() 
