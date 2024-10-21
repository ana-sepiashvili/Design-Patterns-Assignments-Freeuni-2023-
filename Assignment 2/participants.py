import random
from dataclasses import dataclass
from typing import Protocol

from discount import Discount
from generator import Generator
from item import Item
from payment import PayWithCard, PayWithCash
from receipt import Receipt
from repository import Repository


class Cashier(Protocol):
    def open_receipt(self, receipt: Receipt) -> None:
        pass

    def register_items(self, items: list[Item]) -> None:
        pass

    def print_receipt(self) -> None:
        pass

    @staticmethod
    def get_discounted_price(discount: Discount) -> float:
        pass

    def confirm_payment(self, price: float, payment_method: str) -> None:
        pass

    def get_receipt(self) -> Receipt:
        pass

    def make_x_report(self) -> None:
        pass

    def make_z_report(
        self, z_sales_report: Repository, z_revenue_report: Repository
    ) -> None:
        pass


@dataclass
class StoreCashier:
    sales_reports: Repository
    revenue_reports: Repository
    receipt: Receipt = None

    def open_receipt(self, receipt: Receipt) -> None:
        print("- Cashier opens the receipt.")
        self.receipt = receipt

    def register_items(self, items: list[Item]) -> None:
        print("- Cashier registers items one by one in the receipt.")
        for item in items:
            self.receipt.add_item(item)

    def print_receipt(self) -> None:
        print(str(self.receipt))

    @staticmethod
    def get_discounted_price(discount: Discount) -> float:
        print("Final discounted price is ", discount.get_price())

        return discount.get_price()

    def confirm_payment(self, price: float, payment_method: str) -> None:
        for item in self.receipt.get_list():
            self.sales_reports.update((item.get_name(), item.get_amount()))
        self.revenue_reports.update((payment_method, price))

    def get_receipt(self) -> Receipt:
        return self.receipt

    def make_x_report(self) -> None:
        print(str(self.sales_reports))
        print(str(self.revenue_reports))

    def make_z_report(
        self, z_sales_report: Repository, z_revenue_report: Repository
    ) -> None:
        for sale in self.sales_reports.read():
            z_sales_report.update(sale)
        for revenue in self.revenue_reports.read():
            z_revenue_report.update(revenue)

        print(str(z_sales_report))
        print(str(z_revenue_report))


class Customer(Protocol):
    def chosen_products(self) -> list[Item]:
        pass

    def choose_payment_method(self) -> str:
        pass


class StoreCustomer:
    def __init__(self, generator: Generator) -> None:
        self.generator = generator
        print("- Customer with randomly selected items arrive at POS.")

    def chosen_products(self) -> list[Item]:
        return self.generator.get_random_products()

    @staticmethod
    def choose_payment_method() -> str:
        payment = random.choice([PayWithCash(), PayWithCard()])
        return payment.payment_method()
