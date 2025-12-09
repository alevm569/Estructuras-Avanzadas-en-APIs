# API de Gestión de Productos y Pedidos  
## Descripción
Este proyecto desarrolla una API para gestionar productos y pedidos utilizando FastAPI.  
Se emplean estructuras de datos implementadas manualmente:

- **Árbol Binario de Búsqueda (BST)** para productos  
- **Lista Enlazada Simple (LinkedList)** para pedidos  
- **Guardado en JSON** para guardar los datos

## Arquitectura
```
app/
 ├── routers/
 │     ├── products.py
 │     └── orders.py
 ├── storage.py
 ├── schema.py
 └── main.py
data/
 ├── products.json
 └── orders.json
README.md
requirements.txt
```
## Estructuras de datos
### Árbol binario de búsqueda - productos
Permite búsquedas eficientes por ID.
```
             (10)
            /    \
        (4)       (15)
       /  \      /   \
    (2)  (7)   (12)   (20)
```
Cada nodo almacena:
- id del producto (clave)
- datos del producto
- referencia a nodo izquierdo
- referencia a nodo derecho
### Lista Enlazada - pedidos
Cada pedido es un nodo que apunta al siguiente.
```
[Pedido 1] -> [Pedido 2] -> [Pedido 3] -> None
```
Cada nodo contiene:
- datos del pedido
- un puntero al siguiente nodo
### Guardado de datos
Los datos se guardan automáticamente en:

- `data/products.json`
- `data/orders.json`

Se cargan al iniciar el servidor.

## Rutas de la API
### Productos
- POST `/products`
- GET `/products`
- GET `/products/{id}`
- PUT `/products/{id}`
- DELETE `/products/{id}`
- 
Estructura de un producto
```json
{
  "id": 1,
  "name": "Camiseta",
  "price": 15.5,
  "description": "Camiseta unisex"
}
```
### Pedidos
- POST `/orders`
- GET `/orders`
- GET `/orders/{id}`
- PUT `/orders/{id}`
- DELETE `/orders/{id}`

Estructura de un pedido
```json
{
  "id": 100,
  "customer_name": "Ana",
  "items": [
    { "product_id": 1, "name": "Camiseta", "price": 15.5, "quantity": 2 },
    { "product_id": 2, "name": "Gorra", "price": 10.0, "quantity": 1 }
  ],
  "total": 41.0
}

```
  
## Ejecución del proyecto
### Instalación de dependencias
```
pip install -r requirements.txt
```

Contenido del `requirements.txt`:
```
fastapi
uvicorn
pydantic
```
### Ejecución de la API
```
uvicorn app.main:app --reload
```
### Conclusiones y Observaciones
- JSON permite persistencia sin usar bases de datos.
- El BST permite búsquedas muy eficientes, pero no está balanceado; si los IDs son muy desordenados, puede volverse profundo.
- La lista enlazada funciona bien para agregar pedidos y recorrerlos, pero no es rápida para búsquedas masivas (toca recorrer nodo por nodo).
- La modularización del proyecto (routers + storage + schemas) facilita el mantenimiento.

### URL
https://github.com/alevm569/Estructuras-Avanzadas-en-APIs
