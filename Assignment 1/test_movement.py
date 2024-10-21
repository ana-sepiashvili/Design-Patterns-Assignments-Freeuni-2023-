from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from constants import (
    CRAWL_REQUIRED_STAMINA,
    CRAWL_SPEED,
    CRAWL_USES_STAMINA,
    FLY_REQUIRED_STAMINA,
    FLY_SPEED,
    FLY_USES_STAMINA,
    HOP_REQUIRED_STAMINA,
    HOP_SPEED,
    HOP_USES_STAMINA,
    RUN_REQUIRED_STAMINA,
    RUN_SPEED,
    RUN_USES_STAMINA,
    WALK_REQUIRED_STAMINA,
    WALK_SPEED,
    WALK_USES_STAMINA,
)
from features import FakeFeatures, Features


class Movement(Protocol):
    def perform_move(self, features: Features) -> None:
        pass

    def move(self, features: Features) -> None:
        pass


class NoMovement:
    def perform_move(self, features: Features) -> None:
        pass

    def move(self, features: Features) -> None:
        pass


@dataclass
class MovementBase:
    following: Movement

    def can_move(self, features: Features) -> bool:
        raise NotImplementedError

    def perform_move(self, features: Features) -> None:
        raise NotImplementedError

    def move(self, features: Features) -> None:
        if not self.can_move(features):
            return self.following.move(features)
        self.perform_move(features)


@dataclass
class Crawl(MovementBase):
    following: Movement = field(default_factory=NoMovement)

    def can_move(self, features: Features) -> bool:
        return features.get_stamina() >= CRAWL_REQUIRED_STAMINA

    def perform_move(self, features: Features) -> None:
        features.use_stamina_by(CRAWL_USES_STAMINA)
        features.increment_location(CRAWL_SPEED)


@dataclass
class Hop(MovementBase):
    following: Movement = field(default_factory=NoMovement)

    def can_move(self, features: Features) -> bool:
        return (features.get_stamina() >= HOP_REQUIRED_STAMINA
                and features.get_legs() >= 1)

    def perform_move(self, features: Features) -> None:
        features.use_stamina_by(HOP_USES_STAMINA)
        features.increment_location(HOP_SPEED)


@dataclass
class Walk(MovementBase):
    following: Movement = field(default_factory=NoMovement)

    def can_move(self, features: Features) -> bool:
        return (features.get_stamina() >= WALK_REQUIRED_STAMINA
                and features.get_legs() == 2)

    def perform_move(self, features: Features) -> None:
        features.use_stamina_by(WALK_USES_STAMINA)
        features.increment_location(WALK_SPEED)


@dataclass
class Run(MovementBase):
    following: Movement = field(default_factory=NoMovement)

    def can_move(self, features: Features) -> bool:
        return (features.get_stamina() >= RUN_REQUIRED_STAMINA
                and features.get_legs() == 2)

    def perform_move(self, features: Features) -> None:
        features.use_stamina_by(RUN_USES_STAMINA)
        features.increment_location(RUN_SPEED)


@dataclass
class Fly(MovementBase):
    following: Movement = field(default_factory=NoMovement)

    def can_move(self, features: Features) -> bool:
        return (features.get_stamina() >= FLY_REQUIRED_STAMINA
                and features.get_wings() == 2)

    def perform_move(self, features: Features) -> None:
        features.use_stamina_by(FLY_USES_STAMINA)
        features.increment_location(FLY_SPEED)


def test_crawl() -> None:
    features = FakeFeatures(False, stamina=2)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Crawl().move(features)

    assert features.get_location() == previous_location + CRAWL_SPEED
    assert features.get_stamina() == previous_stamina - CRAWL_USES_STAMINA


def test_crawl_with_not_enough_requirements() -> None:
    features = FakeFeatures(False, stamina=0)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Crawl().move(features)

    assert features.get_location() == previous_location
    assert features.get_stamina() == previous_stamina


def test_hop() -> None:
    features = FakeFeatures(True, stamina=25, legs=2)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Hop().move(features)

    assert features.get_location() == previous_location + HOP_SPEED
    assert features.get_stamina() == previous_stamina - HOP_USES_STAMINA


def test_hop_with_not_enough_requirements() -> None:
    features = FakeFeatures(True, stamina=25, legs=0)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Hop().move(features)

    assert features.get_location() == previous_location
    assert features.get_stamina() == previous_stamina


def test_walk() -> None:
    features = FakeFeatures(True, stamina=50, legs=2)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Walk().move(features)

    assert features.get_location() == previous_location + WALK_SPEED
    assert features.get_stamina() == previous_stamina - WALK_USES_STAMINA


def test_walk_with_not_enough_requirements() -> None:
    features = FakeFeatures(True, stamina=30, legs=2)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Walk().move(features)

    assert features.get_location() == previous_location
    assert features.get_stamina() == previous_stamina


def test_run() -> None:
    features = FakeFeatures(True, stamina=70, legs=2)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Run().move(features)

    assert features.get_location() == previous_location + RUN_SPEED
    assert features.get_stamina() == previous_stamina - RUN_USES_STAMINA


def test_run_with_not_enough_requirements() -> None:
    features = FakeFeatures(True, stamina=30, legs=1)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Run().move(features)

    assert features.get_location() == previous_location
    assert features.get_stamina() == previous_stamina


def test_fly() -> None:
    features = FakeFeatures(False, stamina=81, wings=2)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Fly().move(features)

    assert features.get_location() == previous_location + FLY_SPEED
    assert features.get_stamina() == previous_stamina - FLY_USES_STAMINA


def test_fly_with_not_enough_requirements() -> None:
    features = FakeFeatures(True, stamina=88, wings=0)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Fly().move(features)

    assert features.get_location() == previous_location
    assert features.get_stamina() == previous_stamina


def test_chain() -> None:
    features = FakeFeatures(True, stamina=40, wings=0, legs=1)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Fly(Hop(Crawl())).move(features)

    # not enough features for flying but enough for hopping
    assert features.get_location() == previous_location + HOP_SPEED
    assert features.get_stamina() == previous_stamina - HOP_USES_STAMINA


def test_move_twice() -> None:
    features = FakeFeatures(True, stamina=100, wings=2)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Fly().move(features)
    Fly().move(features)

    assert features.get_location() == previous_location + 2 * FLY_SPEED
    assert features.get_stamina() == previous_stamina - 2 * FLY_USES_STAMINA


def test_crawl_multiple_times_with_not_enough_stamina() -> None:
    features = FakeFeatures(False, stamina=1)
    previous_location = features.get_location()
    previous_stamina = features.get_stamina()
    Crawl().move(features)
    Crawl().move(features)
    Crawl().move(features)
    Crawl().move(features)

    assert features.get_location() == previous_location + CRAWL_SPEED
    assert features.get_stamina() == previous_stamina - CRAWL_USES_STAMINA
