from dataclasses import dataclass
from typing import Protocol


@dataclass
class Sales:
    n_receipts: int = 0
    revenue: int = 0

    def get_n_receipts(self) -> int:
        return self.n_receipts

    def get_revenue(self) -> int:
        return self.revenue


class SalesRepository(Protocol):
    def read(self) -> Sales:
        pass
