
import sys
import re
import pytest
from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK
sys.path.append(".")
from main import app

@pytest.fixture(scope="function")
def client() -> TestClient:
    "start the client"
    return TestClient(app)

# def test_vehicles(client:TestClient):
#     response_vehicles = client.get('/api/v1/insert_vehicles')
#     assert response_vehicles.json()["message"] == "insercion de vehiculos exitosa"

# def test_delegaciones(client:TestClient):
#     response_delegaciones = client.get('/api/v1/insert_delegaciones')
#     assert response_delegaciones.json()["Respuesta"]=='Datos insertados satisfactoriamente!'


def test_all_delegaciones(client:TestClient):
    response = client.get('/api/v1/obtener_delegaciones')
    assert len(response.json()) == 16
    assert response.json()[0]["id"] == 2 
    assert response.json()[0]["nombre"] == "María Antonieta Hidalgo Torres" 

def test_get_all_vehicles(client:TestClient):
    response = client.get('/api/v1/get_all_vehicles')
    assert len(response.json()) == 31
    assert response.json()[0]["id"] == 3 
    assert response.json()[0]["vehicle_label"] == 119 
def test_get_relation_vehicles_delegations(client:TestClient):
    response = client.get('/api/v1/get_relation_vehicles_delegations')
    assert len(response.json()) == 10
    assert response.json()["Coyoacán"]["vehicles_ids"][0] == 170 

def test_get_relation_vehicles_delegations(client:TestClient):
    response = client.get('/api/v1/vehicles/170')
    
    assert response.json()["position_latitude"] == 19.3174991607666 
    assert response.json()["position_longitude"] == -99.18779754638672 

