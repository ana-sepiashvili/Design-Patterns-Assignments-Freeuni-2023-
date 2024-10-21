import random

from constants import CLAW_SIZES


class Features:
    def __init__(self, is_prey: bool) -> None:
        self.is_prey = is_prey
        self.location = 0
        if self.is_prey:
            self.location = random.randint(0, 1000)
        self.stamina = random.randint(100, 1000)
        self.health = random.randint(0, 100)
        self.power = random.randint(0, 100)
        self.legs = random.randint(0, 2)
        self.wings = random.randint(0, 2)
        self.claws = random.randint(2, 4)
        self.teeth = random.choice([3, 6, 9])

    def log_characteristics(self) -> None:
        if self.is_prey:
            print("\nPrey was evolved.")
        else:
            print("\nPredator was evolved.")
        print("Location:", self.location)
        print("Stamina:", self.stamina)
        print("Health:", self.health)
        print("Power:", self.power)
        print("Number of legs:", self.legs)
        print("Number of wings:", self.wings)
        print("Claws:", CLAW_SIZES[self.claws - 2])
        print("Teeth with sharpness that boost attacking power with +"
              + str(self.teeth))

    """ Methods For Chasing """

    def use_stamina_by(self, number: int) -> None:
        self.stamina -= number

    def increment_location(self, speed: int) -> None:
        self.location += speed

    """ Methods For Fighting """

    def decrement_health_by(self, damage: int) -> None:
        self.health -= damage

    def multiply_power(self) -> None:
        self.power *= self.claws

    def boost_power(self) -> None:
        self.power += self.teeth

    """ Getter Methods """

    def get_stamina(self) -> int:
        return self.stamina

    def get_location(self) -> int:
        return self.location

    def get_legs(self) -> int:
        return self.legs

    def get_wings(self) -> int:
        return self.wings

    def get_health(self) -> int:
        return self.health

    def get_power(self) -> int:
        return self.power

    def get_teeth(self) -> int:
        return self.teeth

    def get_claws(self) -> int:
        return self.claws


class FakeFeatures(Features):
    def __init__(self, is_prey: bool, location: int = 0, stamina: int = 5,
                 health: int = 5, power: int = 5, legs: int = 5, wings: int = 5,
                 claws: str = "Small", teeth: int = 3) -> None:
        super().__init__(is_prey)
        self.is_prey = is_prey
        self.location = location
        self.stamina = stamina
        self.health = health
        self.power = power
        self.legs = legs
        self.wings = wings
        self.claws = CLAW_SIZES.index(claws) + 2
        self.teeth = teeth

    def use_stamina_by(self, number: int) -> None:
        self.stamina -= number

    def increment_location(self, speed: int) -> None:
        self.location += speed

    """ Methods For Fighting """

    def decrement_health_by(self, damage: int) -> None:
        self.health -= damage

    def multiply_power(self) -> None:
        self.power *= self.claws

    def boost_power(self) -> None:
        self.power += self.teeth

    """ Getter Methods """

    def get_stamina(self) -> int:
        return self.stamina

    def get_location(self) -> int:
        return self.location

    def get_legs(self) -> int:
        return self.legs

    def get_health(self) -> int:
        return self.health

    def get_power(self) -> int:
        return self.power


def test_predator_location() -> None:
    predator_features = Features(False)

    assert predator_features.get_location() == 0


def test_prey_location() -> None:
    prey_features = Features(False)

    assert 0 <= prey_features.get_location() <= 1000


def test_use_stamina_by() -> None:
    features = Features(True)
    previous_stamina = features.get_stamina()
    features.use_stamina_by(1)

    assert features.get_stamina() == previous_stamina - 1


def test_increment_location_by() -> None:
    features = Features(False)
    previous_location = features.get_location()
    features.increment_location(1)

    assert features.get_location() == previous_location + 1


def test_decrement_health_by() -> None:
    features = Features(True)
    previous_health = features.get_health()
    features.decrement_health_by(1)

    assert features.get_health() == previous_health - 1


def test_boost_power() -> None:
    features = Features(True)
    previous_power = features.get_power()
    features.boost_power()

    assert features.get_power() == previous_power + features.get_teeth()


def test_multiply_power() -> None:
    features = Features(True)
    previous_power = features.get_power()
    features.multiply_power()

    assert features.get_power() == previous_power * features.get_claws()
