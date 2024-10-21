from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.errors import DoesNotExistError, ReceiptClosedError
from core.product_in_receipt import ProductInReceipt
from core.receipt import Receipt, ReceiptProtocol
from infra.fastapi.dependables import (
    ProductRepositoryDependable,
    ReceiptRepositoryDependable,
)

receipt_api = APIRouter(tags=["Receipts"])


class ProductInReceiptItem(BaseModel):
    id: UUID
    quantity: int
    price: int
    total: int


class ReceiptItem(BaseModel):
    id: UUID
    status: str
    products: list[ProductInReceiptItem]
    total: int


class ReceiptItemEnvelope(BaseModel):
    receipt: ReceiptItem


@receipt_api.post("/receipts", status_code=201, response_model=ReceiptItemEnvelope)
def create_receipt(receipts: ReceiptRepositoryDependable) -> dict[str, Receipt]:
    receipt = Receipt()
    receipts.add(receipt)
    return {"receipt": receipt}


class AddProductRequest(BaseModel):
    id: UUID
    quantity: int


@receipt_api.post(
    "/receipts/{receipt_id}/products",
    status_code=201,
    response_model=ReceiptItemEnvelope,
)
def add_product(
    receipt_id: UUID,
    request: AddProductRequest,
    receipts: ReceiptRepositoryDependable,
    products: ProductRepositoryDependable,
) -> dict[str, ReceiptProtocol]:
    args = request.model_dump()
    product = products.read(args["id"])
    product_in_receipt = ProductInReceipt(
        args["id"],
        int(args["quantity"]),
        product.get_price(),
        product.get_price() * int(args["quantity"]),
    )

    receipts.add_product(receipt_id, product_in_receipt)
    receipt = receipts.read(receipt_id)
    return {"receipt": receipt}


@receipt_api.get(
    "/receipts/{receipt_id}", status_code=200, response_model=ReceiptItemEnvelope
)
def read_receipt(
    receipt_id: UUID, receipts: ReceiptRepositoryDependable
) -> dict[str, ReceiptProtocol] | JSONResponse:
    try:
        receipt = receipts.read(receipt_id)
        return {"receipt": receipt}
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={
                "error": {"message": f"Receipt with id<{receipt_id}> does not exist."}
            },
        )


class CloseReceiptRequest(BaseModel):
    status: str


@receipt_api.patch("/receipts/{receipt_id}", status_code=200, response_model=Dict)
def close_receipt(
    receipt_id: UUID,
    request: CloseReceiptRequest,
    receipts: ReceiptRepositoryDependable,
) -> dict[str, Any] | JSONResponse:
    try:
        args = request.model_dump()
        receipts.close(receipt_id, args["status"])
        return {}
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={
                "error": {"message": f"Receipt with id<{receipt_id}> does not exist."}
            },
        )


@receipt_api.delete("/receipts/{receipt_id}", status_code=200, response_model=Dict)
def delete_receipt(
    receipt_id: UUID,
    receipts: ReceiptRepositoryDependable,
) -> dict[str, Any] | JSONResponse:
    try:
        receipts.delete(receipt_id)
        return {}
    except ReceiptClosedError:
        return JSONResponse(
            status_code=403,
            content={"error": {"message": f"Receipt with id<{receipt_id}> is closed."}},
        )
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={
                "error": {"message": f"Receipt with id<{receipt_id}> does not exist."}
            },
        )
