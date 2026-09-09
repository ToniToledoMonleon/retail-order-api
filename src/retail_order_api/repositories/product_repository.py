from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from retail_order_api.models.product import Product

from retail_order_api.exceptions.product import (
    ProductSkuAlreadyExistsError,
)

def save_product(product_data: dict, db: Session):
    new_product = Product(**product_data)
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
    except IntegrityError:
        db.rollback()
        raise ProductSkuAlreadyExistsError()

    return new_product

def update_product(product: Product, product_data: dict, db: Session):
    for key, value in product_data.items():
        setattr(product, key, value)

    try:
        db.commit()
        db.refresh(product)
        return product

    except IntegrityError:
        db.rollback()
        raise ProductSkuAlreadyExistsError()


def get_products(db: Session):
    statement = select(Product)

    # Scalars devuelve un iterador de los resultados, y luego convertimos a lista
    return db.scalars(statement).all()

def get_product_by_id(product_id: int, db: Session):
    return db.query(Product).filter(Product.id == product_id).first()

def delete_product(product: Product, db: Session):
    db.delete(product)
    db.commit()
