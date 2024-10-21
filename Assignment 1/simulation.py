from __future__ import annotations

from unittest.mock import patch

from creature import Creature
from features import FakeFeatures, Features
from test_movement import Crawl, Fly, Hop, Run, Walk


def chase(predator: Creature, prey: Creature) -> None:
    print("\nWelcome to Chase Phase")
    while predator.get_features().get_location() < prey.get_features().get_location():
        if not predator.has_stamina():
            print("Pray ran into infinity")
            break
        predator.chase()
        prey.chase()


def attack(attacker: Features, attacked: Features) -> None:
    attacker.boost_power()
    attacker.multiply_power()
    attacked.decrement_health_by(attacker.get_power())


def fight(predator: Creature, prey: Creature) -> None:
    print("Welcome to Fight Phase")
    while True:
        attack(predator.get_features(), prey.get_features())
        if prey.is_dead():
            print("Some R-rated things have happened")
            break
        attack(prey.get_features(), predator.get_features())
        if predator.is_dead():
            print("Pray ran into infinity")
            break


def predator_caught_prey(predator: Creature, prey: Creature) -> bool:
    return predator.get_features().get_location() >= prey.get_features().get_location()


def spore() -> None:
    predator = Creature(Features(False), Fly(Run(Walk(Hop(Crawl())))))
    predator.evolve()

    prey = Creature(Features(True), Fly(Run(Walk(Hop(Crawl())))))
    prey.evolve()

    chase(predator, prey)

    if predator_caught_prey(predator, prey):
        fight(predator, prey)


def simulation() -> None:
    for i in range(100):
        spore()


def test_chase_output_predator_failure() -> None:
    with patch('builtins.print') as mock_print:
        predator = Creature(FakeFeatures(False, stamina=5), Crawl())
        prey = Creature(FakeFeatures(True, location=100, stamina=400, legs=2), Run())

        chase(predator, prey)
        expected_output = "Pray ran into infinity"
        mock_print.assert_called_with(expected_output)


def test_chase_output_predator_catches_prey() -> None:
    with patch('builtins.print') as mock_print:
        predator = Creature(FakeFeatures(False, stamina=100, legs=2), Crawl())
        prey = Creature(FakeFeatures(True, location=1, stamina=0), Run())

        chase(predator, prey)
        mock_print.assert_called()


def test_attack() -> None:
    predator = FakeFeatures(False, power=1, teeth=3, claws="Small")
    prey = FakeFeatures(True, health=10)
    attack(predator, prey)
    # power = (1 + 3) * 2 = 8
    assert prey.get_health() == 2


def test_fight_output_predator_failure() -> None:
    with patch('builtins.print') as mock_print:
        predator = Creature(FakeFeatures(False, power=0, health=0), Crawl())
        prey = Creature(FakeFeatures(True, health=100), Crawl())

        fight(predator, prey)
        expected_output = "Pray ran into infinity"
        mock_print.assert_called_with(expected_output)


def test_fight_output_predator_win() -> None:
    with patch('builtins.print') as mock_print:
        predator = Creature(FakeFeatures(False, power=100), Crawl())
        prey = Creature(FakeFeatures(True, health=0), Crawl())

        fight(predator, prey)
        expected_output = "Some R-rated things have happened"
        mock_print.assert_called_with(expected_output)
