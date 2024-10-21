from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass
class ProductInReceipt:
    id: UUID
    quantity: int
    price: int
    total: int

    def get_id(self) -> UUID:
        return self.id

    def get_quantity(self) -> int:
        return self.quantity

    def get_price(self) -> int:
        return self.price

    def get_total(self) -> int:
        self.total = self.price * self.quantity
        return self.total


class ProductsInReceiptRepository(Protocol):
    def create(self) -> None:
        pass

    def add(self, product: ProductInReceipt) -> None:
        pass

    def read_all(self) -> list[ProductInReceipt]:
        pass

    def delete(self) -> None:
        pass
