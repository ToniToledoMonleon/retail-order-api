from sqlalchemy.orm import Session
from retail_order_api.models.product import Product

def save_product(product_data: dict, db: Session):
    new_product = Product(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

def update_product(product: Product, product_data: dict, db: Session):
    for key, value in product_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)

    return product

def get_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(product_id: int, db: Session):
    return db.query(Product).filter(Product.id == product_id).first()

def delete_product(product_id: int, db: Session):
    product = get_product_by_id(product_id, db)
    if product is None:
        return False, product
    
    db.delete(product)
    db.commit()
    return True, product