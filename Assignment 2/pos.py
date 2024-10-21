import typer

from constants import (
    DATABASE_NAME,
    NUMBER_OF_SHIFTS,
    PRODUCTS_DEFAULT_VALUES,
    PRODUCTS_TABLE_COLUMNS,
    PRODUCTS_TABLE_NAME,
    RANGE_FOR_X_REPORT,
    RANGE_FOR_Z_REPORT,
    REVENUE_REPORT_DEFAULT_VALUES,
    REVENUE_REPORT_TABLE_COLUMNS,
    SALES_REPORT_TABLE_COLUMNS,
    X_REVENUE_REPORT_TABLE_NAME,
    X_SALES_REPORT_TABLE_NAME,
    Z_REVENUE_REPORT_TABLE_NAME,
    Z_SALES_REPORT_TABLE_NAME,
)
from discount import StoreDiscount
from generator import ProductsGenerator
from participants import Cashier, StoreCashier, StoreCustomer
from receipt import ItemsReceipt
from repository import (
    ItemRepository,
    RevenueReportRepository,
    SalesReportRepository,
    SQLiteHandler,
)

app = typer.Typer()


class Simulation:
    def __init__(self) -> None:
        self.sql_handler = SQLiteHandler(DATABASE_NAME)
        self.items_repository = ItemRepository(
            self.sql_handler,
            PRODUCTS_TABLE_NAME,
            PRODUCTS_TABLE_COLUMNS,
            PRODUCTS_DEFAULT_VALUES,
        )
        self.generator = ProductsGenerator(self.items_repository)
        self.z_sales_reports = SalesReportRepository(
            self.sql_handler, Z_SALES_REPORT_TABLE_NAME, SALES_REPORT_TABLE_COLUMNS
        )
        self.z_revenue_reports = RevenueReportRepository(
            self.sql_handler,
            Z_REVENUE_REPORT_TABLE_NAME,
            REVENUE_REPORT_TABLE_COLUMNS,
            REVENUE_REPORT_DEFAULT_VALUES,
        )

    def total_report(self) -> None:
        print(str(self.z_sales_reports))
        print(str(self.z_revenue_reports))

    def list_items(self) -> None:
        print(str(self.items_repository))
        StoreDiscount(
            self.generator.get_all_products(), ItemsReceipt()
        ).print_discounts()

    def simulation(self) -> None:
        for i in range(NUMBER_OF_SHIFTS):
            x_sales_reports = SalesReportRepository(
                self.sql_handler,
                X_SALES_REPORT_TABLE_NAME,
                SALES_REPORT_TABLE_COLUMNS,
            )
            x_sales_reports.create()
            x_revenue_reports = RevenueReportRepository(
                self.sql_handler,
                X_REVENUE_REPORT_TABLE_NAME,
                REVENUE_REPORT_TABLE_COLUMNS,
                REVENUE_REPORT_DEFAULT_VALUES,
            )
            x_revenue_reports.create()
            cashier = StoreCashier(x_sales_reports, x_revenue_reports)
            customer_index = 0
            self.shift(cashier, customer_index)

    def shift(self, cashier: Cashier, customer_index: int) -> None:
        while True:
            customer_index += 1
            customer = StoreCustomer(self.generator)
            cashier.open_receipt(ItemsReceipt())
            cashier.register_items(customer.chosen_products())
            cashier.print_receipt()
            price = cashier.get_discounted_price(
                StoreDiscount(self.generator.get_all_products(), cashier.get_receipt())
            )
            payment_method = customer.choose_payment_method()
            cashier.confirm_payment(price, payment_method)

            if customer_index % RANGE_FOR_X_REPORT == 0:
                user_input = typer.prompt(
                    "Would you like to make X report? (y/n)"
                ).lower()
                if user_input == "y":
                    cashier.make_x_report()

            if customer_index % RANGE_FOR_Z_REPORT == 0:
                user_input = typer.prompt(
                    "Would you like to end the shift and make Z report? (y/n)"
                ).lower()
                if user_input == "y":
                    cashier.make_z_report(self.z_sales_reports, self.z_revenue_reports)
                    break


@app.command("list")
def list_command() -> None:
    s.list_items()


@app.command()
def report() -> None:
    s.total_report()


@app.command()
def simulate() -> None:
    s.simulation()


if __name__ == "__main__":
    s = Simulation()
    app()
