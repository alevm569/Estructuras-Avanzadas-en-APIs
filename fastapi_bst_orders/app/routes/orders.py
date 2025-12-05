from fastapi import APIRouter, HTTPException, status
from typing import List
from ..schema import OrderCreate, OrderOut

from app.storage import (
    insert_order,
    find_order,
    delete_order,
    list_orders,
    get_product,       # para obtener info de productos desde el BST
)

router = APIRouter(prefix="/orders", tags=["orders"])


def build_order_response(order_dict):
    """
    Construye el detalle del pedido incluyendo:
    - datos del producto (si existe en el BST)
    - total calculado
    """
    items_detailed = []
    total = 0.0

    for item in order_dict["items"]:
        prod = get_product(item["product_id"])

        if prod:
            items_detailed.append({
                "product_id": prod["id"],
                "name": prod["name"],
                "price": prod["price"],
                "quantity": item["quantity"]
            })
            total += prod["price"] * item["quantity"]
        else:
            # Producto no existe
            items_detailed.append({
                "product_id": item["product_id"],
                "name": None,
                "price": None,
                "quantity": item["quantity"]
            })

    return {
        "id": order_dict["id"],
        "customer_name": order_dict["customer_name"],
        "items": items_detailed,
        "total": round(total, 2)
    }


# ---------------------------
#        CREATE ORDER
# ---------------------------
@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order_endpoint(order: OrderCreate):

    existing = find_order(order.id)
    if existing:
        raise HTTPException(status_code=400, detail="ID de pedido ya existe")

    insert_order(order.dict())
    return build_order_response(order.dict())


# ---------------------------
#        LIST ORDERS
# ---------------------------
@router.get("", response_model=List[OrderOut])
def list_orders_endpoint():
    all_orders = list_orders()
    return [build_order_response(o) for o in all_orders]


# ---------------------------
#         GET ORDER
# ---------------------------
@router.get("/{order_id}", response_model=OrderOut)
def get_order_endpoint(order_id: int):
    node = find_order(order_id)
    if not node:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return build_order_response(node.order)


# ---------------------------
#       UPDATE ORDER
# ---------------------------
@router.put("/{order_id}", response_model=OrderOut)
def update_order_endpoint(order_id: int, order: OrderCreate):

    node = find_order(order_id)
    if not node:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    if order_id != order.id:
        raise HTTPException(status_code=400, detail="El ID del body y la URL no coinciden")

    # Sobrescribir pedido completo dentro del nodo
    node.order = order.dict()

    # Persistir en archivo JSON
    from app.storage import save_orders
    save_orders()

    return build_order_response(node.order)


# ---------------------------
#        DELETE ORDER
# ---------------------------
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_endpoint(order_id: int):

    deleted = delete_order(order_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    return
