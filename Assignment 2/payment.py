from dataclasses import dataclass
from typing import Protocol


class Payment(Protocol):
    def payment_method(self) -> str:
        pass


@dataclass
class PayWithCash:
    payment: str = "Cash"

    def payment_method(self) -> str:
        print("Customer paid with cash.")
        return self.payment


@dataclass
class PayWithCard:
    payment: str = "Card"

    def payment_method(self) -> str:
        print("Customer paid with card.")
        return self.payment
