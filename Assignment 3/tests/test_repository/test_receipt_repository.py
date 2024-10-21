import uuid

import pytest

from core.errors import DoesNotExistError, ReceiptClosedError
from core.receipt import Receipt
from infra.repositories.database import DatabaseHandler
from infra.repositories.receipt_repository import SqlReceiptRepository
from runner.constants import RECEIPTS_TABLE_COLUMNS, TEST_DATABASE_NAME
from tests.fake import Fake


@pytest.fixture
def database() -> DatabaseHandler:
    db = DatabaseHandler(TEST_DATABASE_NAME)
    return db


def test_receipt_repository_create(database: DatabaseHandler) -> None:
    repository = SqlReceiptRepository(
        database, "test_receipt_create", RECEIPTS_TABLE_COLUMNS
    )
    repository.create()
    receipt = Receipt()
    repository.add(receipt)

    assert repository.read(receipt.get_id()) == receipt


def test_receipt_repository_add_product(database: DatabaseHandler) -> None:
    repository = SqlReceiptRepository(
        database, "test_receipt_add_product", RECEIPTS_TABLE_COLUMNS
    )
    repository.create()
    receipt = Receipt()
    repository.add(receipt)
    product = Fake().product_in_receipt()
    repository.add_product(receipt.get_id(), product)
    receipt.add_product(product)

    assert repository.read(receipt.get_id()) == receipt


def test_receipt_repository_read_empty(database: DatabaseHandler) -> None:
    repository = SqlReceiptRepository(
        database, "test_receipt_read_empty", RECEIPTS_TABLE_COLUMNS
    )
    repository.create()

    with pytest.raises(DoesNotExistError):
        unknown_id = uuid.uuid4()
        repository.read(unknown_id)


def test_receipt_repository_close(database: DatabaseHandler) -> None:
    repository = SqlReceiptRepository(
        database, "test_receipt_close", RECEIPTS_TABLE_COLUMNS
    )
    repository.create()

    receipt = Receipt()
    repository.add(receipt)

    receipt.close()
    repository.close(receipt.get_id(), "closed")
    assert repository.read(receipt.get_id()) == receipt


def test_receipt_repository_close_nonexistent(database: DatabaseHandler) -> None:
    repository = SqlReceiptRepository(
        database, "test_receipt_close_nonexistent", RECEIPTS_TABLE_COLUMNS
    )
    repository.create()

    unknown_id = uuid.uuid4()
    with pytest.raises(DoesNotExistError):
        repository.close(unknown_id, "close")


def test_receipt_repository_delete(database: DatabaseHandler) -> None:
    repository = SqlReceiptRepository(
        database, "test_receipt_delete", RECEIPTS_TABLE_COLUMNS
    )
    repository.create()

    receipt = Receipt()
    repository.add(receipt)

    repository.delete(receipt.get_id())
    with pytest.raises(DoesNotExistError):
        repository.read(receipt.get_id())


def test_receipt_repository_delete_nonexistent(database: DatabaseHandler) -> None:
    repository = SqlReceiptRepository(
        database, "test_receipt_delete_nonexistent", RECEIPTS_TABLE_COLUMNS
    )
    repository.create()

    unknown_id = uuid.uuid4()
    with pytest.raises(DoesNotExistError):
        repository.delete(unknown_id)


def test_receipt_repository_delete_closed(database: DatabaseHandler) -> None:
    repository = SqlReceiptRepository(
        database, "test_receipt_delete_closed", RECEIPTS_TABLE_COLUMNS
    )
    repository.create()

    receipt = Receipt()
    repository.add(receipt)
    repository.close(receipt.get_id(), "closed")

    with pytest.raises(ReceiptClosedError):
        repository.delete(receipt.get_id())
