from discount import StoreDiscount
from item import PackOfItems, SingleItem
from receipt import ItemsReceipt


def test_discount_get_price() -> None:
    discount = StoreDiscount(
        [],
        ItemsReceipt([SingleItem("water", 1.0, 50), SingleItem("beer", 2.5, 0)]),
    )
    assert discount.get_price() == 3.0


def test_discount_get_price_with_pack() -> None:
    discount = StoreDiscount(
        [],
        ItemsReceipt(
            [PackOfItems(SingleItem("water", 1.0, 50), 2), SingleItem("beer", 3.0, 0)]
        ),
    )
    assert discount.get_price() == 3.6


def test_discount_get_price_with_with_prime_number() -> None:
    discount = StoreDiscount([], ItemsReceipt([SingleItem("water", 1.0, 0)]), 2)
    assert discount.get_price() == 0.83
