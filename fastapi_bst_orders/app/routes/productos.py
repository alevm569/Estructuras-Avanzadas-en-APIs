from fastapi import APIRouter, HTTPException, status
from typing import List
from ..schema import ProductCreate, ProductOut

from ..storage import (
    insert_product,
    get_product,
    list_products,
    delete_product 
)

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(p: ProductCreate):
    insert_product(p.dict())
    return p


@router.get("", response_model=List[ProductOut])
def list_products_endpoint():
    return list_products()


@router.get("/{product_id}", response_model=ProductOut)
def get_product_endpoint(product_id: int):
    prod = get_product(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod


@router.put("/{product_id}", response_model=ProductOut)
def update_product_endpoint(product_id: int, p: ProductCreate):
    if product_id != p.id:
        raise HTTPException(
            status_code=400, 
            detail="El ID del body y la ruta deben coincidir"
        )

    existing = get_product(product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    insert_product(p.dict())
    return p


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(product_id: int):
    deleted = delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return
