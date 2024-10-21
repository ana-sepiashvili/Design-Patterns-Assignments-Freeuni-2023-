import random
from dataclasses import dataclass
from typing import Protocol

from constants import MAX_ITEMS_AMOUNT, MIN_ITEMS_AMOUNT
from item import Item, PackOfItems, SingleItem
from repository import Repository


@dataclass
class Generator(Protocol):
    repository: Repository

    def get_all_products(self) -> list[Item]:
        pass

    def get_random_products(self) -> list[Item]:
        pass


@dataclass
class ProductsGenerator:
    repository: Repository

    def get_all_products(self) -> list[Item]:
        result = []
        for item in self.repository.read():
            if item[1] == 1:
                product = SingleItem(item[0], item[2], item[3])
            else:
                product = PackOfItems(SingleItem(item[0], item[2], item[3]), item[1])
            result.append(product)
        return result

    def get_random_products(self) -> list[Item]:
        all_products = self.get_all_products()
        number_of_products = random.randint(MIN_ITEMS_AMOUNT, MAX_ITEMS_AMOUNT)
        random_indexes = [
            random.randint(0, len(all_products) - 1) for _ in range(number_of_products)
        ]
        chosen_products = []
        for index in random_indexes:
            chosen_products.append(all_products[index])
        return chosen_products
