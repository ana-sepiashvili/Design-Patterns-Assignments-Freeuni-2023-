import uuid
from unittest.mock import ANY
from uuid import uuid4

import pytest
from starlette.testclient import TestClient

from runner.constants import TEST_DATABASE_NAME_WITH_UNIT
from runner.setup import init_app
from runner.setup_database import create_database
from tests.fake import Fake


@pytest.fixture
def client() -> TestClient:
    create_database(TEST_DATABASE_NAME_WITH_UNIT)
    return TestClient(init_app(TEST_DATABASE_NAME_WITH_UNIT))


def test_should_create(client: TestClient) -> None:
    product = Fake().product()

    response = client.post("/products", json=product)

    assert response.status_code == 201
    assert response.json() == {"product": {"id": ANY, **product}}


def test_should_not_create_with_unknown_unit(client: TestClient) -> None:
    product = Fake().product()
    unknown_id = uuid4()
    product["unit_id"] = str(unknown_id)
    response = client.post("/products", json=product)
    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Unit with id<{unknown_id}> does not exist."}
    }


def test_should_not_read_unknown(client: TestClient) -> None:
    unknown_id = uuid4()
    response = client.get(f"/products/{unknown_id}")
    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Product with id<{unknown_id}> does not exist."}
    }


def test_should_create_existed(client: TestClient) -> None:
    product = Fake().product()
    client.post("/products", json=product)

    response = client.post("/products", json=product)
    barcode = product["barcode"]
    assert response.status_code == 409
    assert response.json() == {
        "error": {"message": f"Product with barcode<{barcode}> already exists."}
    }


def test_should_persist(client: TestClient) -> None:
    product = Fake().product()

    response = client.post("/products", json=product)
    product_id = response.json()["product"]["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json() == {"product": {"id": product_id, **product}}


def test_get_all_units_on_empty(client: TestClient) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == {"products": []}


def test_get_all_units(client: TestClient) -> None:
    product = Fake().product()

    response = client.post("/products", json=product)
    product_id = response.json()["product"]["id"]

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == {"products": [{"id": product_id, **product}]}


def test_should_update(client: TestClient) -> None:
    product = Fake().product()

    response = client.post("/products", json=product)
    product_id = response.json()["product"]["id"]

    response = client.patch(f"/products/{product_id}", json={"price": 10})

    assert response.status_code == 200
    assert response.json() == {}


def test_should_update_nonexistent(client: TestClient) -> None:
    unknown_id = uuid.uuid4()
    response = client.patch(f"/products/{unknown_id}", json={"price": 10})
    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Product with id<{unknown_id}> does not exist."}
    }
