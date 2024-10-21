from constants import (
    REVENUE_REPORT_DEFAULT_VALUES,
    REVENUE_REPORT_TABLE_COLUMNS,
    SALES_REPORT_TABLE_COLUMNS,
)
from item import SingleItem
from participants import StoreCashier
from receipt import ItemsReceipt
from repository import RevenueReportRepository, SalesReportRepository, SQLiteHandler


def test_cashier_receipt() -> None:
    sqlhandler = SQLiteHandler("test.db")
    sales = SalesReportRepository(sqlhandler, "sales", SALES_REPORT_TABLE_COLUMNS)
    revenues = RevenueReportRepository(
        sqlhandler,
        "revenue",
        REVENUE_REPORT_TABLE_COLUMNS,
        REVENUE_REPORT_DEFAULT_VALUES,
    )
    cashier = StoreCashier(sales, revenues)
    cashier.open_receipt(ItemsReceipt())
    assert cashier.get_receipt() == ItemsReceipt()


def test_cashier_register_items() -> None:
    sqlhandler = SQLiteHandler("test.db")
    sales = SalesReportRepository(sqlhandler, "sales", SALES_REPORT_TABLE_COLUMNS)
    revenues = RevenueReportRepository(
        sqlhandler,
        "revenue",
        REVENUE_REPORT_TABLE_COLUMNS,
        REVENUE_REPORT_DEFAULT_VALUES,
    )

    cashier = StoreCashier(sales, revenues)
    cashier.open_receipt(ItemsReceipt())
    cashier.register_items([SingleItem("item", 1.0, 0)])
    assert cashier.get_receipt().get_list() == [SingleItem("item", 1.0, 0)]


def test_cashier_confirm_payment() -> None:
    sqlhandler = SQLiteHandler("test.db")
    sales = SalesReportRepository(
        sqlhandler, "sales_confirm_payment", SALES_REPORT_TABLE_COLUMNS
    )
    sales.create()
    revenues = RevenueReportRepository(
        sqlhandler,
        "revenue_confirm_payment",
        REVENUE_REPORT_TABLE_COLUMNS,
        REVENUE_REPORT_DEFAULT_VALUES,
    )
    revenues.create()

    cashier = StoreCashier(sales, revenues)
    cashier.open_receipt(ItemsReceipt())
    cashier.register_items([SingleItem("item", 1.0, 0)])
    cashier.confirm_payment(1.0, "Cash")
    assert sales.read() == [("item", 1)]
    assert revenues.read() == [("Cash", 1.0), ("Card", 0.0)]


def test_cashier_make_z_reports() -> None:
    sqlhandler = SQLiteHandler("test.db")
    sales = SalesReportRepository(sqlhandler, "sales_x", SALES_REPORT_TABLE_COLUMNS)
    sales.create()
    sales.update(("item_x", 5))
    revenues = RevenueReportRepository(
        sqlhandler,
        "revenue_x",
        REVENUE_REPORT_TABLE_COLUMNS,
        REVENUE_REPORT_DEFAULT_VALUES,
    )
    revenues.create()
    revenues.update(("Card", 10.0))

    z_sales = SalesReportRepository(sqlhandler, "sales_z", SALES_REPORT_TABLE_COLUMNS)
    z_sales.create()
    z_revenues = RevenueReportRepository(
        sqlhandler,
        "revenue_z",
        REVENUE_REPORT_TABLE_COLUMNS,
        REVENUE_REPORT_DEFAULT_VALUES,
    )
    z_revenues.create()

    cashier = StoreCashier(sales, revenues)
    cashier.make_z_report(z_sales, z_revenues)
    assert z_sales.read() == [("item_x", 5)]
    assert z_revenues.read() == [("Cash", 0.0), ("Card", 10.0)]
