import pytest

from infra.repositories.database import DatabaseHandler
from infra.repositories.products_in_receipt_repository import (
    SqlProductsInReceiptRepository,
)
from runner.constants import PRODUCTS_IN_REPOSITORY_COLUMNS, TEST_DATABASE_NAME
from tests.fake import Fake


@pytest.fixture
def database() -> DatabaseHandler:
    db = DatabaseHandler(TEST_DATABASE_NAME)
    return db


def test_products_in_receipt_create_table(database: DatabaseHandler) -> None:
    repository = SqlProductsInReceiptRepository(
        database,
        "test_products_in_receipt_create_table",
        PRODUCTS_IN_REPOSITORY_COLUMNS,
    )
    repository.create()
    assert len(repository.read_all()) == 0


def test_products_in_receipt_create(database: DatabaseHandler) -> None:
    repository = SqlProductsInReceiptRepository(
        database,
        "test_products_in_receipt_create",
        PRODUCTS_IN_REPOSITORY_COLUMNS,
    )
    repository.create()
    product = Fake().product_in_receipt()
    repository.add(product)
    assert len(repository.read_all()) == 1
    assert repository.read_all()[0] == product


def test_products_in_receipt_read_all(database: DatabaseHandler) -> None:
    repository = SqlProductsInReceiptRepository(
        database,
        "test_products_in_receipt_read_all",
        PRODUCTS_IN_REPOSITORY_COLUMNS,
    )
    repository.create()
    product1 = Fake().product_in_receipt()
    product2 = Fake().product_in_receipt()
    product3 = Fake().product_in_receipt()

    repository.add(product1)
    repository.add(product2)
    repository.add(product3)

    assert len(repository.read_all()) == 3
    assert repository.read_all()[0] == product1
    assert repository.read_all()[1] == product2
    assert repository.read_all()[2] == product3
