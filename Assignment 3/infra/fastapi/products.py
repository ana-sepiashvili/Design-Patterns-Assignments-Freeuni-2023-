from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.errors import DoesNotExistError, ExistsError
from core.product import Product
from infra.fastapi.dependables import (
    ProductRepositoryDependable,
    UnitRepositoryDependable,
)

product_api = APIRouter(tags=["Products"])


class CreateProductRequest(BaseModel):
    unit_id: UUID
    name: str
    barcode: str
    price: int


class UpdateProductRequest(BaseModel):
    price: int


class ProductItem(BaseModel):
    id: UUID
    unit_id: UUID
    name: str
    barcode: str
    price: int


class ProductItemEnvelope(BaseModel):
    product: ProductItem


class ProductListEnvelope(BaseModel):
    products: list[ProductItem]


@product_api.post("/products", status_code=201, response_model=ProductItemEnvelope)
def create_product(
    request: CreateProductRequest,
    products: ProductRepositoryDependable,
    units: UnitRepositoryDependable,
) -> dict[str, Any] | JSONResponse:
    product = Product(**request.model_dump())
    try:
        units.read(product.get_unit_id())
        try:
            products.add(product)
            return {"product": product}
        except ExistsError:
            return JSONResponse(
                status_code=409,
                content={
                    "error": {
                        "message": f"Product with "
                        f"barcode<{product.get_barcode()}> already exists."
                    }
                },
            )
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "message": f"Unit with id<{product.get_unit_id()}> does not exist."
                }
            },
        )


@product_api.get(
    "/products/{product_id}", status_code=200, response_model=ProductItemEnvelope
)
def read_product(
    product_id: UUID, products: ProductRepositoryDependable
) -> dict[str, Product] | JSONResponse:
    try:
        product = products.read(product_id)
        return {"product": product}
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={
                "error": {"message": f"Product with id<{product_id}> does not exist."}
            },
        )


@product_api.get("/products", status_code=200, response_model=ProductListEnvelope)
def read_all(products: ProductRepositoryDependable) -> dict[str, Any]:
    return {"products": products.read_all()}


@product_api.patch("/products/{product_id}", status_code=200, response_model=Dict)
def update_product(
    product_id: UUID,
    request: UpdateProductRequest,
    products: ProductRepositoryDependable,
) -> dict[str, Any] | JSONResponse:
    try:
        products.update(product_id, **request.model_dump())
        return {}
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={
                "error": {"message": f"Product with id<{product_id}> does not exist."}
            },
        )
