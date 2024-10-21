import uuid

import pytest

from core.errors import DoesNotExistError, ExistsError
from core.product import Product
from infra.repositories.database import DatabaseHandler
from infra.repositories.product_repository import SqlProductRepository
from runner.constants import PRODUCTS_TABLE_COLUMNS, TEST_DATABASE_NAME


@pytest.fixture
def database() -> DatabaseHandler:
    db = DatabaseHandler(TEST_DATABASE_NAME)
    return db


def test_product_repository_create_table(database: DatabaseHandler) -> None:
    repository = SqlProductRepository(
        database, "test_product_create_table", PRODUCTS_TABLE_COLUMNS
    )
    repository.create()

    assert len(repository.read_all()) == 0


def test_product_repository_create(database: DatabaseHandler) -> None:
    repository = SqlProductRepository(
        database, "test_products_create", PRODUCTS_TABLE_COLUMNS
    )
    repository.create()

    repository.add(Product(uuid.uuid4(), "product_name", "barcode", 10))
    assert len(repository.read_all()) == 1


def test_product_repository_create_exists(database: DatabaseHandler) -> None:
    repository = SqlProductRepository(
        database, "test_products_create_exists", PRODUCTS_TABLE_COLUMNS
    )
    repository.create()

    repository.add(Product(uuid.uuid4(), "product_name1", "barcode", 10))
    with pytest.raises(ExistsError):
        repository.add(Product(uuid.uuid4(), "product_name2", "barcode", 10))


def test_product_repository_read_empty(database: DatabaseHandler) -> None:
    repository = SqlProductRepository(
        database, "test_product_read_empty", PRODUCTS_TABLE_COLUMNS
    )
    repository.create()

    with pytest.raises(DoesNotExistError):
        unknown_id = uuid.uuid4()
        repository.read(unknown_id)


def test_product_repository_read(database: DatabaseHandler) -> None:
    repository = SqlProductRepository(
        database, "test_product_read", PRODUCTS_TABLE_COLUMNS
    )
    repository.create()

    product = Product(uuid.uuid4(), "product_name", "barcode", 10)
    repository.add(product)
    assert repository.read(product.get_id()) == product


def test_product_repository_read_all(database: DatabaseHandler) -> None:
    repository = SqlProductRepository(
        database, "test_product_read_all", PRODUCTS_TABLE_COLUMNS
    )
    repository.create()

    product1 = Product(uuid.uuid4(), "product1", "barcode1", 10)
    product2 = Product(uuid.uuid4(), "product2", "barcode2", 10)
    repository.add(product1)
    repository.add(product2)

    result = repository.read_all()
    assert len(result) == 2
    assert result[0] == product1
    assert result[1] == product2


def test_product_repository_update(database: DatabaseHandler) -> None:
    repository = SqlProductRepository(
        database, "test_product_update", PRODUCTS_TABLE_COLUMNS
    )
    repository.create()

    product = Product(uuid.uuid4(), "product", "barcode", 10)
    repository.add(product)
    repository.update(product.get_id(), 20)

    assert repository.read(product.get_id()).get_price() == 20


def test_product_repository_update_nonexistent(database: DatabaseHandler) -> None:
    repository = SqlProductRepository(
        database, "test_product_update_nonexistent", PRODUCTS_TABLE_COLUMNS
    )
    repository.create()

    with pytest.raises(DoesNotExistError):
        unknown_id = uuid.uuid4()
        repository.update(unknown_id, 20)
