import uuid

import pytest

from core.errors import DoesNotExistError, ExistsError
from core.unit import Unit
from infra.repositories.database import DatabaseHandler
from infra.repositories.unit_repository import SqlUnitRepository
from runner.constants import TEST_DATABASE_NAME, UNITS_TABLE_COLUMNS


@pytest.fixture
def database() -> DatabaseHandler:
    db = DatabaseHandler(TEST_DATABASE_NAME)
    return db


def test_unit_repository_create_table(database: DatabaseHandler) -> None:
    repository = SqlUnitRepository(
        database, "test_units_create_table", UNITS_TABLE_COLUMNS
    )
    repository.create()
    assert len(repository.read_all()) == 0


def test_unit_repository_create(database: DatabaseHandler) -> None:
    repository = SqlUnitRepository(database, "test_units_create", UNITS_TABLE_COLUMNS)
    repository.create()
    repository.add(Unit("unit_name"))
    assert len(repository.read_all()) == 1


def test_unit_repository_create_exists(database: DatabaseHandler) -> None:
    repository = SqlUnitRepository(
        database, "test_units_create_exists", UNITS_TABLE_COLUMNS
    )
    repository.create()
    repository.add(Unit("unit_name"))
    with pytest.raises(ExistsError):
        repository.add(Unit("unit_name"))


def test_unit_repository_read_empty(database: DatabaseHandler) -> None:
    repository = SqlUnitRepository(
        database, "test_units_read_empty", UNITS_TABLE_COLUMNS
    )
    repository.create()
    with pytest.raises(DoesNotExistError):
        unknown_id = uuid.uuid4()
        repository.read(unknown_id)


def test_unit_repository_read(database: DatabaseHandler) -> None:
    repository = SqlUnitRepository(database, "test_units_read", UNITS_TABLE_COLUMNS)
    repository.create()
    unit = Unit("unit_name")
    repository.add(unit)
    assert repository.read(unit.get_id()) == unit


def test_unit_repository_read_all(database: DatabaseHandler) -> None:
    repository = SqlUnitRepository(database, "test_units_read_all", UNITS_TABLE_COLUMNS)
    repository.create()

    unit1 = Unit("unit1")
    unit2 = Unit("unit2")
    repository.add(unit1)
    repository.add(unit2)

    result = repository.read_all()
    assert len(result) == 2
    assert result[0] == unit1
    assert result[1] == unit2
