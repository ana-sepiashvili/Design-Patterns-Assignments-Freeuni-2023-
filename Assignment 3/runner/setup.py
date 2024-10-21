from fastapi import FastAPI

from infra.fastapi.products import product_api
from infra.fastapi.receipts import receipt_api
from infra.fastapi.sales import sales_api
from infra.fastapi.units import unit_api
from infra.repositories.database import DatabaseHandler
from infra.repositories.product_repository import SqlProductRepository
from infra.repositories.receipt_repository import SqlReceiptRepository
from infra.repositories.sales_repository import SqlSalesRepository
from infra.repositories.unit_repository import SqlUnitRepository
from runner.constants import (
    PRODUCTS_TABLE_COLUMNS,
    PRODUCTS_TABLE_NAME,
    RECEIPTS_TABLE_COLUMNS,
    RECEIPTS_TABLE_NAME,
    UNITS_TABLE_COLUMNS,
    UNITS_TABLE_NAME,
)


def init_app(db_name: str) -> FastAPI:
    app = FastAPI()
    app.include_router(unit_api)
    app.include_router(product_api)
    app.include_router(receipt_api)
    app.include_router(sales_api)

    db = DatabaseHandler(db_name)
    app.state.units = SqlUnitRepository(db, UNITS_TABLE_NAME, UNITS_TABLE_COLUMNS)
    app.state.products = SqlProductRepository(
        db, PRODUCTS_TABLE_NAME, PRODUCTS_TABLE_COLUMNS
    )
    app.state.receipts = SqlReceiptRepository(
        db, RECEIPTS_TABLE_NAME, RECEIPTS_TABLE_COLUMNS
    )
    app.state.sales = SqlSalesRepository(db, RECEIPTS_TABLE_NAME)

    return app
