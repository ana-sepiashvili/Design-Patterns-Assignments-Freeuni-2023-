from unittest.mock import ANY
from uuid import uuid4

import pytest
from starlette.testclient import TestClient

from runner.constants import TEST_DATABASE_NAME
from runner.setup import init_app
from runner.setup_database import create_database
from tests.fake import Fake


@pytest.fixture
def client() -> TestClient:
    create_database(TEST_DATABASE_NAME)
    return TestClient(init_app(TEST_DATABASE_NAME))


def test_should_not_read_unknown(client: TestClient) -> None:
    unknown_id = uuid4()

    response = client.get(f"/units/{unknown_id}")
    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Unit with id<{unknown_id}> does not exist."}
    }


def test_should_create(client: TestClient) -> None:
    unit = Fake().unit()

    response = client.post("/units", json=unit)

    assert response.status_code == 201
    assert response.json() == {"unit": {"id": ANY, **unit}}


def test_should_create_existed(client: TestClient) -> None:
    unit = Fake().unit()
    client.post("/units", json=unit)

    response = client.post("/units", json=unit)
    unit_name = unit["name"]
    assert response.status_code == 409
    assert response.json() == {
        "error": {"message": f"Unit with name<{unit_name}> already exists."}
    }


def test_should_persist(client: TestClient) -> None:
    unit = Fake().unit()

    response = client.post("/units", json=unit)
    unit_id = response.json()["unit"]["id"]

    response = client.get(f"/units/{unit_id}")

    assert response.status_code == 200
    assert response.json() == {"unit": {"id": unit_id, **unit}}


def test_get_all_units_on_empty(client: TestClient) -> None:
    response = client.get("/units")

    assert response.status_code == 200
    assert response.json() == {"units": []}


def test_get_all_units(client: TestClient) -> None:
    unit = Fake().unit()

    response = client.post("/units", json=unit)
    unit_id = response.json()["unit"]["id"]

    response = client.get("/units")

    assert response.status_code == 200
    assert response.json() == {"units": [{"id": unit_id, **unit}]}
