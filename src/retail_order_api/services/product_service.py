
from retail_order_api.repositories.product_repository import delete_product, get_product_by_id, get_products, save_product


class ProductNotFoundError(Exception):
    pass 

class ProductStockNotAvailableError(Exception):
    pass

def save_product_service(product_data: dict):
    try:
        return save_product(product_data.model_dump())
    except Exception as e:
        raise ProductNotFoundError()

def modify_product_service(product_id: int, product_data: dict):
    product = get_product_by_id(product_id)
    if product is None:
        raise ProductNotFoundError()
    
    if product["stock"] <= 0:
        raise ProductStockNotAvailableError()

    product.update(product_data.model_dump())
    return product

def get_product_service(product_id: int):
    product = get_product_by_id(product_id)
    if product is None:
        raise ProductNotFoundError()
    
    if product["stock"] <= 0:
        raise ProductStockNotAvailableError()

    return product

def get_products_service():
    products = get_products()
    return products

def delete_product_service(product_id: int):
    deleted, product = delete_product(product_id)
    if not deleted:
        raise ProductNotFoundError()

    return product