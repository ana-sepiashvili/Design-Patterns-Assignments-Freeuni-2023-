import pytest
from starlette.testclient import TestClient

from core.receipt import Receipt
from core.sales import Sales
from runner.constants import (
    TEST_DATABASE_NAME_WITH_PRODUCT,
    TEST_PRODUCT_ID,
    TEST_PRODUCT_PRICE,
)
from runner.setup import init_app
from runner.setup_database import create_database


@pytest.fixture
def client() -> TestClient:
    create_database(TEST_DATABASE_NAME_WITH_PRODUCT)
    return TestClient(init_app(TEST_DATABASE_NAME_WITH_PRODUCT))


def test_report_empty(client: TestClient) -> None:
    response = client.get("/sales")

    assert response.status_code == 200
    assert response.json() == {"sales": {"n_receipts": 0, "revenue": 0}}


def test_report(client: TestClient) -> None:
    receipt = Receipt()
    product_in_receipt = {"id": TEST_PRODUCT_ID, "quantity": 5}
    client.post("/receipts")
    client.post(f"/receipts/{receipt.get_id()}/products", json=product_in_receipt)
    response = client.get("/sales")
    sales = Sales(1, TEST_PRODUCT_PRICE * 5)
    assert response.status_code == 200
    assert response.json() == {
        "sales": {"n_receipts": sales.get_n_receipts(), "revenue": sales.get_revenue()}
    }
