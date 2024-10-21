from constants import (
    PRODUCTS_DEFAULT_VALUES,
    PRODUCTS_TABLE_COLUMNS,
    REVENUE_REPORT_DEFAULT_VALUES,
    REVENUE_REPORT_TABLE_COLUMNS,
    SALES_REPORT_TABLE_COLUMNS,
)
from repository import (
    ItemRepository,
    RevenueReportRepository,
    SalesReportRepository,
    SQLiteHandler,
)


def test_item_repository_create() -> None:
    sqlhandler = SQLiteHandler("test.db")
    repo = ItemRepository(
        sqlhandler, "test_items_create", PRODUCTS_TABLE_COLUMNS, PRODUCTS_DEFAULT_VALUES
    )
    repo.create()
    assert len(repo.read()) == len(PRODUCTS_DEFAULT_VALUES)


def test_item_repository_read_element() -> None:
    sqlhandler = SQLiteHandler("test.db")
    values = (("item1", 1, 2.0, 0),)
    repo = ItemRepository(sqlhandler, "test_items_read", PRODUCTS_TABLE_COLUMNS, values)
    repo.create()
    assert repo.read()[0] == ("item1", 1, 2.0, 0)


def test_item_repository_update() -> None:
    sqlhandler = SQLiteHandler("test.db")
    repo = ItemRepository(
        sqlhandler, "test_items_update", PRODUCTS_TABLE_COLUMNS, PRODUCTS_DEFAULT_VALUES
    )
    repo.create()
    repo.update(("item", 1, 1.0, 5))
    assert len(repo.read()) == len(PRODUCTS_DEFAULT_VALUES) + 1


def test_sales_report_repository_create() -> None:
    sqlhandler = SQLiteHandler("test.db")
    repo = SalesReportRepository(sqlhandler, "sales_create", SALES_REPORT_TABLE_COLUMNS)
    repo.create()
    assert len(repo.read()) == 0


def test_sales_report_repository_update_insert() -> None:
    sqlhandler = SQLiteHandler("test.db")
    repo = SalesReportRepository(sqlhandler, "sales_update", SALES_REPORT_TABLE_COLUMNS)
    repo.create()
    repo.update(("item1", 5))
    assert len(repo.read()) == 1


def test_sales_report_repository_update_increment() -> None:
    sqlhandler = SQLiteHandler("test.db")
    repo = SalesReportRepository(
        sqlhandler, "sales_update_twice", SALES_REPORT_TABLE_COLUMNS
    )
    repo.create()
    repo.update(("item1", 5))
    repo.update(("item1", 5))
    assert repo.read()[0][1] == 10


def test_revenue_report_create() -> None:
    sqlhandler = SQLiteHandler("test.db")
    repo = RevenueReportRepository(
        sqlhandler,
        "revenue_create",
        REVENUE_REPORT_TABLE_COLUMNS,
        REVENUE_REPORT_DEFAULT_VALUES,
    )
    repo.create()
    assert len(repo.read()) == len(REVENUE_REPORT_DEFAULT_VALUES)


def test_revenue_report_read() -> None:
    sqlhandler = SQLiteHandler("test.db")
    repo = RevenueReportRepository(
        sqlhandler,
        "revenue_read",
        REVENUE_REPORT_TABLE_COLUMNS,
        REVENUE_REPORT_DEFAULT_VALUES,
    )
    repo.create()
    assert repo.read() == [("Cash", 0.0), ("Card", 0.0)]


def test_revenue_report_update() -> None:
    sqlhandler = SQLiteHandler("test.db")
    repo = RevenueReportRepository(
        sqlhandler,
        "revenue_update",
        REVENUE_REPORT_TABLE_COLUMNS,
        REVENUE_REPORT_DEFAULT_VALUES,
    )
    repo.create()
    repo.update(("Cash", 5.0))
    assert repo.read() == [("Cash", 5.0), ("Card", 0.0)]
