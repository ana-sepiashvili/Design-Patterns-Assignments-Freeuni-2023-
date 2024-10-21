from dataclasses import dataclass, field
from typing import Protocol

from item import Item


@dataclass
class Receipt(Protocol):
    def add_item(self, item: Item) -> None:
        pass

    def calculate_total_price(self) -> float:
        pass

    def get_list(self) -> list[Item]:
        pass

    def __str__(self) -> str:
        pass


@dataclass
class ItemsReceipt:
    items: list[Item] = field(default_factory=list)

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def calculate_total_price(self) -> float:
        total = 0.0
        for item in self.items:
            total += item.get_discounted_price() * item.get_amount()
        return total

    def get_list(self) -> list[Item]:
        return self.items

    def __str__(self) -> str:
        result = (
            "\nProduct        | Units | Price |  Total  |\n"
            + "---------------|-------|-------|---------|\n"
        )
        for item in self.items:
            discounted_price = item.get_discounted_price()
            result += (
                f"{item.get_name()}{' ' * (15 - len(item.get_name()))}|"
                + f"  {item.get_amount()}{' ' * (5 - len(str(item.get_amount())))}|"
                + f"  {discounted_price}"
                + f"{' ' * (5 - len(str(discounted_price)))}|"
                + f"  {discounted_price * item.get_amount()}"
                + f"{' ' * (7 - len(str(discounted_price * item.get_amount())))}|\n"
            )
        return result
