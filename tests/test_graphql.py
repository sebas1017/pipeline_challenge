from graphene.test import Client
import pytest
from starlette.testclient import TestClient
import sys
import os 
import graphene
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from delegacion.repository import graphql

@pytest.fixture(scope="module")
def client():
    client = Client(schema=graphene.Schema(query=graphql.Query))
    return client

def test_mutation_post(client:TestClient):
    query = """
        query{
            allDelegaciones{
              id
              delegacion
            }
        }
    """
    result = client.execute(query)
    print(result)
    # assert result["data"]["allDelegaciones"]["ok"] == True