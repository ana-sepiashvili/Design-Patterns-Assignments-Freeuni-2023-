from item import PackOfItems, SingleItem


def test_single_item_zero_discount() -> None:
    item = SingleItem("water", 1.0, 0)
    assert item.get_discounted_price() == 1.0


def test_single_item_nonzero_discount() -> None:
    item = SingleItem("water", 1.0, 10)
    assert item.get_discounted_price() == 0.9


def test_single_item_amount() -> None:
    item = SingleItem("water", 1.0, 10)
    assert item.get_amount() == 1


def test_pack_of_items_discount() -> None:
    pack = PackOfItems(SingleItem("water", 1.0, 10), 3)
    assert pack.get_discounted_price() == 0.9


def test_pack_of_items_name() -> None:
    pack = PackOfItems(SingleItem("bread", 1.0, 0), 3)

    assert pack.get_name() == "bread"


def test_pack_of_items_price() -> None:
    pack = PackOfItems(SingleItem("bread", 1.0, 0), 3)

    assert pack.get_price() == 1.0


def test_pack_of_items_amount() -> None:
    pack = PackOfItems(SingleItem("bread", 1.0, 0), 3)

    assert pack.get_amount() == 3
