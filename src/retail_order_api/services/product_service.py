
from sqlalchemy.orm import Session

from retail_order_api.repositories.product_repository import delete_product, get_product_by_id, get_products, update_product, save_product

class ProductNotFoundError(Exception):
    pass 

class ProductStockNotAvailableError(Exception):
    pass

def save_product_service(product_data: dict, db: Session):
    return save_product(product_data.model_dump(), db)


def update_product_service(product_id: int, product_data: dict, db: Session):
    product = get_product_by_id(product_id, db)
    
    if product is None:
        raise ProductNotFoundError()
    
    update_data = product_data.model_dump(exclude_unset=True)

    return update_product(product, update_data, db)

def get_product_service(product_id: int, db: Session):
    product = get_product_by_id(product_id, db)
    if product is None:
        raise ProductNotFoundError()
    
    return product

def get_products_service(db: Session):
    products = get_products(db)
    return products

def delete_product_service(product_id: int, db: Session):
    deleted, product = delete_product( product_id, db)
    if not deleted:
        raise ProductNotFoundError()

    return product