from dataclasses import dataclass, field
from unittest.mock import patch

from features import Features
from test_movement import Crawl, Hop, Movement, NoMovement, Run


@dataclass
class Creature:
    features: Features
    movement: Movement = field(default_factory=NoMovement)

    def evolve(self) -> None:
        self.features.log_characteristics()

    def has_stamina(self) -> bool:
        return self.features.get_stamina() > 0

    def chase(self) -> None:
        self.movement.move(self.features)

    def get_features(self) -> Features:
        return self.features

    def is_dead(self) -> bool:
        return self.get_features().get_health() <= 0


def test_evolve_not_empty_output() -> None:
    prey = Creature(Features(True), Run())

    with patch('builtins.print') as mock_print:
        prey.evolve()

    prey_output = ""
    for call_args in mock_print.call_args_list:
        prey_output = call_args[0][0]

    assert len(prey_output) > 0


def test_evolve_creature_has_location_feature() -> None:
    predator = Creature(Features(False), Hop(Crawl()))
    predator.evolve()

    assert predator.get_features().get_location() == 0
