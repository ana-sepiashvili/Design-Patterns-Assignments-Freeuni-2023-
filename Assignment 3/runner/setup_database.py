import uuid

from core.product import Product
from core.unit import Unit
from infra.repositories.database import DatabaseHandler
from infra.repositories.product_repository import SqlProductRepository
from infra.repositories.receipt_repository import SqlReceiptRepository
from infra.repositories.unit_repository import SqlUnitRepository
from runner.constants import (
    DATABASE_NAME,
    PRODUCTS_TABLE_COLUMNS,
    PRODUCTS_TABLE_NAME,
    RECEIPTS_TABLE_COLUMNS,
    RECEIPTS_TABLE_NAME,
    TEST_DATABASE_NAME_WITH_PRODUCT,
    TEST_DATABASE_NAME_WITH_UNIT,
    TEST_PRODUCT_ID,
    TEST_PRODUCT_PRICE,
    TEST_UNIT_ID,
    UNITS_TABLE_COLUMNS,
    UNITS_TABLE_NAME,
)


def create_database(db_name: str) -> None:
    db = DatabaseHandler(db_name)
    unit_repository = SqlUnitRepository(db, UNITS_TABLE_NAME, UNITS_TABLE_COLUMNS)
    unit_repository.create()
    product_repository = SqlProductRepository(
        db, PRODUCTS_TABLE_NAME, PRODUCTS_TABLE_COLUMNS
    )
    product_repository.create()
    insert_default_values(db_name, product_repository, unit_repository)

    receipt_repository = SqlReceiptRepository(
        db, RECEIPTS_TABLE_NAME, RECEIPTS_TABLE_COLUMNS
    )
    receipt_repository.create()


def insert_default_values(
    db_name: str,
    product_repository: SqlProductRepository,
    unit_repository: SqlUnitRepository,
) -> None:
    if db_name == TEST_DATABASE_NAME_WITH_UNIT:
        unit_repository.add(Unit("test_unit_name", uuid.UUID(TEST_UNIT_ID)))
    elif db_name == TEST_DATABASE_NAME_WITH_PRODUCT:
        product_repository.add(
            Product(
                uuid.UUID(TEST_UNIT_ID),
                "test_product_name",
                "12345",
                TEST_PRODUCT_PRICE,
                uuid.UUID(TEST_PRODUCT_ID),
            )
        )


if __name__ == "__main__":
    create_database(DATABASE_NAME)
