from unittest.mock import ANY
from uuid import uuid4

import pytest
from starlette.testclient import TestClient

from core.receipt import Receipt
from runner.constants import (
    TEST_DATABASE_NAME_WITH_PRODUCT,
    TEST_PRODUCT_ID,
    TEST_PRODUCT_PRICE,
)
from runner.setup import init_app
from runner.setup_database import create_database
from tests.fake import Fake


@pytest.fixture
def client() -> TestClient:
    create_database(TEST_DATABASE_NAME_WITH_PRODUCT)
    return TestClient(init_app(TEST_DATABASE_NAME_WITH_PRODUCT))


def test_should_create(client: TestClient) -> None:
    receipt = Fake().receipt()
    response = client.post("/receipts")

    assert response.status_code == 201
    assert response.json() == {"receipt": {"id": ANY, **receipt}}


def test_should_add_product(client: TestClient) -> None:
    receipt = Receipt()
    product_in_receipt = {"id": TEST_PRODUCT_ID, "quantity": 5}
    client.post("/receipts")
    response = client.post(
        f"/receipts/{receipt.get_id()}/products", json=product_in_receipt
    )

    assert response.status_code == 201
    assert response.json() == {
        "receipt": {
            "id": str(receipt.get_id()),
            "status": "open",
            "products": [
                {
                    "id": TEST_PRODUCT_ID,
                    "quantity": 5,
                    "price": TEST_PRODUCT_PRICE,
                    "total": TEST_PRODUCT_PRICE * 5,
                }
            ],
            "total": TEST_PRODUCT_PRICE * 5,
        }
    }


def test_should_not_read_unknown(client: TestClient) -> None:
    unknown_id = uuid4()
    response = client.get(f"/receipts/{unknown_id}")
    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Receipt with id<{unknown_id}> does not exist."}
    }


def test_should_persist(client: TestClient) -> None:
    receipt = Fake().receipt()

    response = client.post("/receipts")
    receipt_id = response.json()["receipt"]["id"]

    response = client.get(f"/receipts/{receipt_id}")

    assert response.status_code == 200
    assert response.json() == {"receipt": {"id": receipt_id, **receipt}}


def test_should_close_receipt(client: TestClient) -> None:
    response = client.post("/receipts")
    receipt_id = response.json()["receipt"]["id"]

    response = client.patch(f"/receipts/{receipt_id}", json={"status": "closed"})

    assert response.status_code == 200
    assert response.json() == {}


def test_should_not_close_nonexistent_receipt(client: TestClient) -> None:
    unknown_id = uuid4()
    response = client.patch(f"/receipts/{unknown_id}", json={"status": "closed"})
    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Receipt with id<{unknown_id}> does not exist."}
    }


def test_should_delete_receipt(client: TestClient) -> None:
    response = client.post("/receipts")
    receipt_id = response.json()["receipt"]["id"]

    response = client.delete(f"/receipts/{receipt_id}")

    assert response.status_code == 200
    assert response.json() == {}


def test_should_not_delete_nonexistent_receipt(client: TestClient) -> None:
    unknown_id = uuid4()
    response = client.delete(
        f"/receipts/{unknown_id}",
    )
    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Receipt with id<{unknown_id}> does not exist."}
    }


def test_should_not_delete_closed_receipt(client: TestClient) -> None:
    response = client.post("/receipts")
    receipt_id = response.json()["receipt"]["id"]
    client.patch(f"/receipts/{receipt_id}", json={"status": "closed"})

    response = client.delete(f"/receipts/{receipt_id}")

    assert response.status_code == 403
    assert response.json() == {
        "error": {"message": f"Receipt with id<{receipt_id}> is closed."}
    }
