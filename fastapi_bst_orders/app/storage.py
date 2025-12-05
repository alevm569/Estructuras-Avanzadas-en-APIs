import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")


# --------------------------------------------
# --- Árbol Binario de Busqueda (BST) ---
# --------------------------------------------

class ProductNode:
    def __init__(self, key, product):
        self.key = key
        self.product = product
        self.left = None
        self.right = None


class ProductBST:
    def __init__(self):
        self.root = None

    def insert(self, key, product):
        def _insert(node, key, product):
            if node is None:
                return ProductNode(key, product)
            if key == node.key:
                node.product = product  
            elif key < node.key:
                node.left = _insert(node.left, key, product)
            else:
                node.right = _insert(node.right, key, product)
            return node

        self.root = _insert(self.root, key, product)

    def search(self, key):
        node = self.root
        while node:
            if key == node.key:
                return node.product
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def to_list(self):
        result = []

        def inorder(node):
            if not node:
                return
            inorder(node.left)
            result.append(node.product)
            inorder(node.right)

        inorder(self.root)
        return result

    def load_from_list(self, products_list):
        self.root = None
        for p in products_list:
            self.insert(p["id"], p)

# --------------------------------------------
# --- Lista enlazada simple para pedidos ---
# --------------------------------------------

class OrderNode:
    def __init__(self, order):
        self.order = order
        self.next = None


class OrderLinkedList:
    def __init__(self):
        self.head = None

    def append(self, order):
        new_node = OrderNode(order)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def find(self, order_id):
        current = self.head
        while current:
            if current.order["id"] == order_id:
                return current
            current = current.next
        return None

    def delete(self, order_id):
        current = self.head
        prev = None

        while current:
            if current.order["id"] == order_id:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next

        return False

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.order)
            current = current.next
        return result

    def load_from_list(self, orders_list):
        self.head = None
        for order in orders_list:
            self.append(order)

# --------------------------------------------
# --- Persistencia JSON ---
# --------------------------------------------

_products_bst = ProductBST()
_orders_list = OrderLinkedList()


def save_products():
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(_products_bst.to_list(), f, indent=2, ensure_ascii=False)


def save_orders():
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(_orders_list.to_list(), f, indent=2, ensure_ascii=False)


def load_data():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            products = json.load(f)
            _products_bst.load_from_list(products)

    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            orders = json.load(f)
            _orders_list.load_from_list(orders)


# Llamar carga al iniciar API
load_data()


# --------------------------------------------
# Funciones que para el router
# --------------------------------------------

def insert_product(product):
    _products_bst.insert(product["id"], product)
    save_products()

def get_product(product_id):
    return _products_bst.search(product_id)

def list_products():
    return _products_bst.to_list()

def delete_product(product_id):
    def _delete(node, key):
        if not node:
            return None, False

        if key < node.key:
            node.left, deleted = _delete(node.left, key)
            return node, deleted

        if key > node.key:
            node.right, deleted = _delete(node.right, key)
            return node, deleted

        # caso: key == node.key 
        if not node.left:
            return node.right, True
        if not node.right:
            return node.left, True

        # nodo con dos hijos - reemplazar por sucesor inorder
        succ = node.right
        while succ.left:
            succ = succ.left

        node.key = succ.key
        node.product = succ.product

        node.right, _ = _delete(node.right, succ.key)
        return node, True

    _products_bst.root, deleted = _delete(_products_bst.root, product_id)

    if deleted:
        save_products()

    return deleted



def insert_order(order):
    _orders_list.append(order)
    save_orders()

def find_order(order_id):
    return _orders_list.find(order_id)

def delete_order(order_id):
    deleted = _orders_list.delete(order_id)
    if deleted:
        save_orders()
    return deleted

def list_orders():
    return _orders_list.to_list()
