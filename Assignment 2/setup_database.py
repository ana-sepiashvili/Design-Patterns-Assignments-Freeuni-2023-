from constants import (
    DATABASE_NAME,
    PRODUCTS_DEFAULT_VALUES,
    PRODUCTS_TABLE_COLUMNS,
    PRODUCTS_TABLE_NAME,
    REVENUE_REPORT_DEFAULT_VALUES,
    REVENUE_REPORT_TABLE_COLUMNS,
    SALES_REPORT_TABLE_COLUMNS,
    Z_REVENUE_REPORT_TABLE_NAME,
    Z_SALES_REPORT_TABLE_NAME,
)
from repository import (
    ItemRepository,
    RevenueReportRepository,
    SalesReportRepository,
    SQLiteHandler,
)


def create_database() -> None:
    sql_handler = SQLiteHandler(DATABASE_NAME)
    items_repository = ItemRepository(
        sql_handler,
        PRODUCTS_TABLE_NAME,
        PRODUCTS_TABLE_COLUMNS,
        PRODUCTS_DEFAULT_VALUES,
    )
    items_repository.create()
    z_sales_reports = SalesReportRepository(
        sql_handler, Z_SALES_REPORT_TABLE_NAME, SALES_REPORT_TABLE_COLUMNS
    )
    z_sales_reports.create()
    z_revenue_reports = RevenueReportRepository(
        sql_handler,
        Z_REVENUE_REPORT_TABLE_NAME,
        REVENUE_REPORT_TABLE_COLUMNS,
        REVENUE_REPORT_DEFAULT_VALUES,
    )
    z_revenue_reports.create()


if __name__ == "__main__":
    create_database()
