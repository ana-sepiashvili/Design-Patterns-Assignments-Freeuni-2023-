import uuid
from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class Unit:
    name: str
    id: UUID = field(default_factory=uuid4)

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> UUID:
        return self.id


class UnitRepository(Protocol):
    def create(self) -> None:
        pass

    def add(self, unit: Unit) -> None:
        pass

    def read(self, unit_id: uuid.UUID) -> Unit:
        pass

    def read_all(self) -> list[Unit]:
        pass
