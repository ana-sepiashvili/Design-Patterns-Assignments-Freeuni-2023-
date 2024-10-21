import uuid
from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class Product:
    unit_id: UUID
    name: str
    barcode: str
    price: int

    id: UUID = field(default_factory=uuid4)

    def get_id(self) -> UUID:
        return self.id

    def get_unit_id(self) -> UUID:
        return self.unit_id

    def get_name(self) -> str:
        return self.name

    def get_barcode(self) -> str:
        return self.barcode

    def get_price(self) -> int:
        return self.price


class ProductRepository(Protocol):
    def create(self) -> None:
        pass

    def add(self, product: Product) -> None:
        pass

    def read(self, product_id: uuid.UUID) -> Product:
        pass

    def read_all(self) -> list[Product]:
        pass

    def update(self, product_id: UUID, price: int) -> None:
        pass
