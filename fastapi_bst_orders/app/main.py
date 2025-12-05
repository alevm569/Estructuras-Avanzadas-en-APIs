from fastapi import FastAPI
from app.routes import productos, orders

app = FastAPI(title="Tienda - API")

app.include_router(productos.router)
app.include_router(orders.router)
