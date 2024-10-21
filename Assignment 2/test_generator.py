from constants import PRODUCTS_TABLE_COLUMNS
from generator import ProductsGenerator
from item import SingleItem
from repository import ItemRepository, SQLiteHandler


def test_generator_all_products_size() -> None:
    values = (
        ("Bread", 1, 2.0, 0),
        ("Milk", 1, 3.5, 10),
    )
    items = ItemRepository(
        SQLiteHandler("test_generator"), "items", PRODUCTS_TABLE_COLUMNS, values
    )
    items.create()
    generator = ProductsGenerator(items)

    assert len(generator.get_all_products()) == len(values)


def test_generator_all_products_first_item() -> None:
    values = (
        ("Bread", 1, 2.0, 0),
        ("Milk", 1, 3.5, 10),
    )
    items = ItemRepository(
        SQLiteHandler("test_generator"), "items1", PRODUCTS_TABLE_COLUMNS, values
    )
    items.create()
    generator = ProductsGenerator(items)

    assert generator.get_all_products()[0] == SingleItem("Bread", 2.0, 0)
