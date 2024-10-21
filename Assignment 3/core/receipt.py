import uuid
from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID

from core.product_in_receipt import ProductInReceipt


class ReceiptProtocol(Protocol):
    def get_id(self) -> UUID:
        pass

    def get_status(self) -> str:
        pass

    def get_products(self) -> list[ProductInReceipt]:
        pass

    def get_total(self) -> int:
        pass

    def add_product(self, product: ProductInReceipt) -> None:
        pass

    def close(self) -> None:
        pass


@dataclass
class Receipt:
    id: UUID = uuid.uuid4()
    status: str = "open"
    products: list[ProductInReceipt] = field(default_factory=list)
    total: int = 0

    def get_id(self) -> UUID:
        return self.id

    def get_status(self) -> str:
        return self.status

    def get_products(self) -> list[ProductInReceipt]:
        return self.products

    def get_total(self) -> int:
        return self.total

    def add_product(self, product: ProductInReceipt) -> None:
        self.total += product.get_total()
        self.products.append(product)

    def close(self) -> None:
        self.status = "closed"


class ReceiptRepository(Protocol):
    def create(self) -> None:
        pass

    def add(self, receipt: ReceiptProtocol) -> None:
        pass

    def add_product(self, receipt_id: UUID, product: ProductInReceipt) -> None:
        pass

    def read(self, receipt_id: UUID) -> ReceiptProtocol:
        pass

    def close(self, receipt_id: UUID, status: str) -> None:
        pass

    def delete(self, receipt_id: UUID) -> None:
        pass
