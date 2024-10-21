from item import PackOfItems, SingleItem
from receipt import ItemsReceipt


def test_receipt_add_item() -> None:
    receipt = ItemsReceipt(
        [SingleItem("water", 1.0, 0), PackOfItems(SingleItem("beer", 2.5, 0), 6)]
    )

    receipt.add_item(SingleItem("test_item", 2.0, 0))
    assert len(receipt.get_list()) == 3


def test_receipt_calculate_price() -> None:
    receipt = ItemsReceipt(
        [SingleItem("water", 1.0, 20), PackOfItems(SingleItem("beer", 2.5, 0), 6)]
    )
    assert receipt.calculate_total_price() == 15.8
