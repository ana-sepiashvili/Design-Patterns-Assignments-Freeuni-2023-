import uuid
from dataclasses import dataclass, field
from typing import Any

from faker import Faker

from core.product_in_receipt import ProductInReceipt
from runner.constants import TEST_UNIT_ID


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def unit(self) -> dict[str, Any]:
        return {"name": self.faker.catch_phrase()}

    def product(self) -> dict[str, Any]:
        return {
            "unit_id": str(TEST_UNIT_ID),
            "name": self.faker.catch_phrase(),
            "barcode": str(self.faker.uuid4())[:12],
            "price": self.faker.random_int(),
        }

    @staticmethod
    def receipt() -> dict[str, Any]:
        return {
            "status": "open",
            "products": [],
            "total": 0,
        }

    def product_in_receipt(self) -> ProductInReceipt:
        quantity = self.faker.random_int()
        price = self.faker.random_int()
        return ProductInReceipt(uuid.uuid4(), quantity, price, quantity * price)
