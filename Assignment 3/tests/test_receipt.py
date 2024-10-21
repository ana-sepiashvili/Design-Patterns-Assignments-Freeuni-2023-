import uuid

from core.product_in_receipt import ProductInReceipt
from core.receipt import Receipt


def test_receipt_get_total_on_empty() -> None:
    receipt = Receipt()
    assert receipt.get_total() == 0


def test_receipt_add_product() -> None:
    receipt = Receipt()
    product = ProductInReceipt(uuid.uuid4(), 2, 10, 20)
    receipt.add_product(product)
    assert receipt.get_products()[0] == product


def test_receipt_get_total() -> None:
    receipt = Receipt()
    product = ProductInReceipt(uuid.uuid4(), 2, 10, 7)
    receipt.add_product(product)
    assert receipt.get_total() == 20


def test_receipt_get_total_multiple() -> None:
    receipt = Receipt()
    product1 = ProductInReceipt(uuid.uuid4(), 2, 10, 7)
    receipt.add_product(product1)

    product2 = ProductInReceipt(uuid.uuid4(), 3, 5, 15)
    receipt.add_product(product2)
    assert receipt.get_total() == 35


def test_receipt_status() -> None:
    receipt = Receipt()
    assert receipt.get_status() == "open"


def test_receipt_close() -> None:
    receipt = Receipt()
    receipt.close()
    assert receipt.get_status() == "closed"
