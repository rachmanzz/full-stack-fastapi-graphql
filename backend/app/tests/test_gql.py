import pytest
import time
import httpx
import json

my_storage = {}

@pytest.fixture
def storage():
    return my_storage


@pytest.mark.asyncio
async def test_create_user(server, credentials, storage):
    query = '''
        mutation {
            userCreate(user: {
                email:"{email}",
                password:"{password}"
            }) {
                success,
                id
            }
        }
    '''
    query = query.replace("{email}", credentials["email"])
    query = query.replace("{password}", credentials["password"])

    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://localhost:8000/gql',
            timeout=60,
            json = { 
            "query": query,
            "variables": None
            })
        json_response = json.loads(response.text)
        print(json_response)
        assert json_response["data"]["userCreate"]["success"] == True
        storage["user_id"] = json_response["data"]["userCreate"]["id"]

@pytest.mark.asyncio
async def test_auth_user(server, credentials, storage):
    query = '''
    mutation {
        authUser(user: {
            email:"{email}",
            password: "{password}"
        }) {
		    tokenType,
          accessToken
        }
    }
    '''
    query = query.replace("{email}", credentials["email"])
    query = query.replace("{password}", credentials["password"])

    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://localhost:8000/gql',
            headers={},
            timeout=60,
            json = { 
            "query": query,
            "variables": None
            })
        json_response = json.loads(response.text)
        assert json_response["data"]["authUser"]["tokenType"] == "bearer"
        assert json_response["data"]["authUser"]["accessToken"] != None
        storage["accessToken"] = json_response["data"]["authUser"]["accessToken"] 


@pytest.mark.asyncio
async def test_create_item(server, storage):
    query = '''
    mutation {
        itemCreate(item: {
            title:"{title}",
            description: "{description}"
        }) {
		    success
        }
    }
    '''
    query = query.replace("{title}", "mytitle")
    query = query.replace("{description}", "mydescription")
    token = storage["accessToken"]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://localhost:8000/gql',
            headers={"Authorization": f"Bearer {token}"},
            timeout=60,
            json = { 
            "query": query,
            "variables": None,
            })
        json_response = json.loads(response.text)

        assert json_response["data"]["itemCreate"]["success"] == True
