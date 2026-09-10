from decimal import Decimal

from sqlalchemy import func, select, or_
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
    except IntegrityError as exc:
        db.rollback()

        constraint_name = getattr(
            getattr(exc.orig, "diag", None),
            "constraint_name",
            None,
        )

        if constraint_name == "uq_products_sku":
            raise ProductSkuAlreadyExistsError() from exc

        raise
    return new_product

def update_product(product: Product, product_data: dict, db: Session):
    for key, value in product_data.items():
        setattr(product, key, value)

    try:
        db.commit()
        db.refresh(product)
        return product

    except IntegrityError as exc:
        db.rollback()

        constraint_name = getattr(
            getattr(exc.orig, "diag", None),
            "constraint_name",
            None,
        )

        if constraint_name == "uq_products_sku":
            raise ProductSkuAlreadyExistsError() from exc

        raise

def get_products(
        active: bool | None, 
        min_price: float | None, 
        max_price: float | None, 
        search: str | None,
        sort_by: str,
        sort_order: str, 
        limit: int, 
        offset: int, 
        db: Session
    ):
    
    statement = select(Product)
    statement = _apply_product_filters(statement, active, min_price, max_price, search)

    sort_columns = {
        "id": Product.id,
        "price": Product.price,
        "stock": Product.stock,
        "created_at": Product.created_at,
    }

    sort_column = sort_columns[sort_by]

    if sort_order == "desc":
        statement = statement.order_by(
            sort_column.desc(),
            Product.id.desc(),
        )

    else:
        statement = statement.order_by(
            sort_column.asc(),
            Product.id.asc(),
        )

    statement = (
        statement
        .offset(offset)
        .limit(limit)
    )

    # Scalars devuelve un iterador de los resultados, y luego convertimos a lista
    return db.scalars(statement).all()

def get_product_by_id(product_id: int, db: Session):
    return db.query(Product).filter(Product.id == product_id).first()

def delete_product(product: Product, db: Session):
    db.delete(product)
    db.commit()

def count_products(
        db: Session,
        active: bool | None,
        min_price: Decimal | None,
        max_price: Decimal | None,
        search: str | None,
    ) -> int:

    statement = select(
        func.count(Product.id)
    )

    statement = _apply_product_filters(
        statement,
        active,
        min_price,
        max_price,
        search,
    )

    return db.scalar(statement) or 0

def _apply_product_filters(statement, 
                           active: bool | None, 
                           min_price: Decimal | None, 
                           max_price: Decimal | None,
                           search: str | None
                        ):
    
    if active is not None:
        statement = statement.where(Product.active == active)

    if min_price is not None:
        statement = statement.where(Product.price >= min_price)

    if max_price is not None:
        statement = statement.where(Product.price <= max_price)

    if search is not None:
        statement = statement.where(
            or_(
                Product.description.ilike(
                    f"%{search}%"
                ),
                Product.sku.ilike(
                    f"%{search}%"
                ),
            )
        )
