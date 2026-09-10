
from decimal import Decimal

from sqlalchemy.orm import Session

from retail_order_api.repositories.product_repository import count_products, delete_product, get_product_by_id, get_products, update_product, save_product
from retail_order_api.exceptions.product import ProductNotFoundError

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

def get_products_service(active: bool | None, 
                         min_price: Decimal | None, 
                         max_price: Decimal | None, 
                         search: str | None, 
                         sort_by: str, 
                         sort_order: str,
                         limit: int, 
                         offset: int, 
                         db: Session
                        ):
    
    products = get_products(active, min_price, max_price, search, sort_by, sort_order, limit, offset, db)
    total = count_products(active, min_price, max_price, search, db)

    return {
            "items": products, 
            "total": total, 
            "limit": limit, 
            "offset": offset
            }

def delete_product_service(product_id: int, db: Session):
    product = get_product_by_id(product_id, db)
    if product is None:
        raise ProductNotFoundError()

    delete_product(product, db)

    return product