from dataclasses import dataclass
from typing import Protocol


class Item(Protocol):
    def get_name(self) -> str:
        pass

    def get_amount(self) -> int:
        pass

    def get_discount(self) -> int:
        pass

    def get_price(self) -> float:
        pass

    def get_discounted_price(self) -> float:
        pass


@dataclass
class SingleItem:
    name: str
    price: float
    discount: int
    amount: int = 1

    def get_name(self) -> str:
        return self.name

    def get_amount(self) -> int:
        return self.amount

    def get_discount(self) -> int:
        return self.discount

    def get_price(self) -> float:
        return self.price

    def get_discounted_price(self) -> float:
        return self.price * (1.0 - self.discount * 0.01)


@dataclass
class PackOfItems:
    item: Item
    amount: int

    def get_name(self) -> str:
        return self.item.get_name()

    def get_amount(self) -> int:
        return self.amount

    def get_discount(self) -> int:
        return self.item.get_discount()

    def get_price(self) -> float:
        return self.item.get_price()

    def get_discounted_price(self) -> float:
        return self.get_price() * (1.0 - self.get_discount() * 0.01)
