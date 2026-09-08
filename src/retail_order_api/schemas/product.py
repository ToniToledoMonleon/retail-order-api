from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    description : str = Field(UNIQUE=True, min_length=1) 
    price : float = Field(gt=0)
    stock : int = Field(ge=0)

class ProductResponse(BaseModel):
    id : int
    description : str
    price : float
    stock : int