from payment import PayWithCard, PayWithCash


def test_pay_with_cash() -> None:
    assert PayWithCash().payment_method() == "Cash"


def test_pay_with_card() -> None:
    assert PayWithCard().payment_method() == "Card"
