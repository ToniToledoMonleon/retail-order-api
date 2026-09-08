from fastapi import FastAPI
from retail_order_api.routers.product_route import router as product_router

app = FastAPI()
app.include_router(product_router, prefix="/api")

@app.get("/")
def get_health():
    return {"status": "ok"}