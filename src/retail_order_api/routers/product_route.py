from fastapi import APIRouter, HTTPException
from retail_order_api.services.product_service import ProductNotFoundError, ProductStockNotAvailableError, delete_product_service, get_products_service, modify_product_service, save_product_service, get_product_service
from retail_order_api.schemas.product import ProductCreate, ProductResponse

router = APIRouter()

@router.post("/products")
def create_product(product_data: ProductCreate):
    try:
        product = save_product_service(product_data)
    
    except ProductStockNotAvailableError:
        raise HTTPException(status_code=400, detail="Product stock not available")

    return{
        "message": "Product created successfully",
        "product": product
    }

@router.get("/products/{product_id}")
def get_product(product_id: int):
    try:
        product = get_product_service(product_id)
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

@router.get("/products")
def get_products():
    products = get_products_service()
    return products
    
@router.put("/products/{product_id}")
def modify_product(product_id: int, product_data: ProductCreate):
    try:
        return modify_product_service(product_id, product_data)
    
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

def delete_product(product_id: int):
    try:
        return delete_product_service(product_id)
    
    except ProductNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )