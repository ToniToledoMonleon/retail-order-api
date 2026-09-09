from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

class ProductCreate(BaseModel):
    description : str = Field(min_length=1, max_length=200) 
    price : Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock : int = Field(ge=0)

class ProductUpdate(BaseModel):
    description : str | None = Field(default=None, min_length=1, max_length=200) 
    price : Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock : int |None = Field(default=None, ge=0)

class ProductResponse(BaseModel):
    id : int
    description : str
    price : Decimal
    stock : int

    model_config = ConfigDict(from_attributes=True)