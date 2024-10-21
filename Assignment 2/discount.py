from dataclasses import dataclass, field
from typing import Protocol

from constants import DISCOUNT_ON_PACKS, DISCOUNT_ON_PRIME_CUSTOMER
from item import Item, PackOfItems
from receipt import Receipt


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True


@dataclass
class Discount(Protocol):
    def get_price(self) -> float:
        pass

    @staticmethod
    def print_discounts() -> None:
        pass


@dataclass
class StoreDiscount:
    all_items: list[Item]
    receipt: Receipt = field(default_factory=Receipt)
    customer_number: int = 0

    def get_price(self) -> float:
        price = self.receipt.calculate_total_price()
        for current_item in self.receipt.get_list():
            if isinstance(current_item, PackOfItems):
                price *= 1.0 - DISCOUNT_ON_PACKS * 0.01

        if is_prime(self.customer_number):
            price *= 1.0 - DISCOUNT_ON_PRIME_CUSTOMER * 0.01

        return price

    @staticmethod
    def print_discounts() -> None:
        result = (
            " Current Discounts!\n"
            + "If you buy pack of any product you get 10% discount of total price!\n"
            + "If your are lucky customer with prime number you get"
            + "-17% off the receipt price!\n"
        )
        # for current_item in self.all_items:
        #     if current_item.get_discount() > 0:
        #         result += (
        #             f"{current_item.get_name()}: {current_item.get_discount()}% off\n"
        #         )
        print(result)
