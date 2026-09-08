products = {
    1: {"id" :1, "description": "Product 1", "price": 10.0, "stock": 5},
    2: {"id" :2, "description": "Product 2", "price": 20.0, "stock": 3},
    3: {"id" :3, "description": "Product 3", "price": 15.0, "stock": 0},
}

def save_product(product_data: dict):
    new_id = max(products.keys()) + 1 if products else 1

    product = {
        "id": new_id,
        **product_data,
    }

    products[new_id] = product
    return product

def get_products():
    return list(products.values())


def get_product_by_id(product_id: int):
    product = products.get(product_id)
    return product

def delete_product(product_id: int):
    product = products.get(product_id)
    if product is None:
        return False
    
    del products[product_id]
    return True, product