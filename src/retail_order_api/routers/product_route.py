from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from retail_order_api.exceptions.product import (
    ProductSkuAlreadyExistsError,
    ProductNotFoundError,
)
from retail_order_api.services.product_service import ProductStockNotAvailableError, delete_product_service, get_products_service, update_product_service, save_product_service, get_product_service
from retail_order_api.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from retail_order_api.db.database import get_db

router = APIRouter()

# Crear un nuevo producto
@router.post("/")
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    try:
        product = save_product_service(product_data, db)

    except ProductSkuAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Product SKU already exists")
    
    except ProductStockNotAvailableError:
        raise HTTPException(status_code=400, detail="Product stock not available")

    return{
        "message": "Product created successfully",
        "product": product
    }

# Obtener un producto por su ID
@router.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = get_product_service(product_id, db)
        return product
    
    except ProductNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    except ProductStockNotAvailableError:
        raise HTTPException(
            status_code=409,
            detail="Product stock not available",
        )
# Obtener todos los productos
@router.get("/products", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return get_products_service(db)

# Actualizar un producto existente   
@router.patch("/products/{product_id}")
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    try:
        return update_product_service(product_id, product_data, db)
    
    except ProductNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    except ProductSkuAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Product SKU already exists",
        )
    
@router.delete("/products/{product_id}", response_model=ProductResponse,)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        return delete_product_service(product_id, db)
    
    except ProductNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )