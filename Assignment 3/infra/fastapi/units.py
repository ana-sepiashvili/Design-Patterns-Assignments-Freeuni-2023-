from typing import Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.errors import DoesNotExistError, ExistsError
from core.unit import Unit
from infra.fastapi.dependables import UnitRepositoryDependable

unit_api = APIRouter(tags=["Units"])


class CreateUnitRequest(BaseModel):
    name: str


class UnitItem(BaseModel):
    id: UUID
    name: str


class UnitItemEnvelope(BaseModel):
    unit: UnitItem


class UnitListEnvelope(BaseModel):
    units: list[UnitItem]


@unit_api.post("/units", status_code=201, response_model=UnitItemEnvelope)
def create_unit(
    request: CreateUnitRequest, units: UnitRepositoryDependable
) -> dict[str, Unit] | JSONResponse:
    unit = Unit(**request.model_dump())
    try:
        units.add(unit)
        return {"unit": unit}
    except ExistsError:
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "message": f"Unit with name<{unit.get_name()}> already exists."
                }
            },
        )


@unit_api.get("/units/{unit_id}", status_code=200, response_model=UnitItemEnvelope)
def read_unit(
    unit_id: UUID, units: UnitRepositoryDependable
) -> dict[str, Unit] | JSONResponse:
    try:
        unit = units.read(unit_id)
        return {"unit": unit}
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={"error": {"message": f"Unit with id<{unit_id}> does not exist."}},
        )


@unit_api.get("/units", status_code=200, response_model=UnitListEnvelope)
def read_all(units: UnitRepositoryDependable) -> dict[str, Any]:
    return {"units": units.read_all()}
