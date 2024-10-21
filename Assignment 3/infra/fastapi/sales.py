from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from infra.fastapi.dependables import SalesRepositoryDependable

sales_api = APIRouter(tags=["Sales"])


class SalesItem(BaseModel):
    n_receipts: int
    revenue: int


class SalesItemEnvelope(BaseModel):
    sales: SalesItem


@sales_api.get("/sales", status_code=200, response_model=SalesItemEnvelope)
def report(sales_repo: SalesRepositoryDependable) -> dict[str, Any]:
    sales = sales_repo.read()
    return {"sales": sales}
