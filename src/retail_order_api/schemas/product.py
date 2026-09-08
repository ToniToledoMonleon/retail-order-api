from pydantic import BaseModel, ConfigDict, Field

class ProductCreate(BaseModel):
    description : str = Field(min_length=1, max_length=200) 
    price : float = Field(gt=0)
    stock : int = Field(ge=0)

class ProductUpdate(BaseModel):
    description : str | None = Field(min_length=1, max_length=200) 
    price : float | None = Field(gt=0)
    stock : int |None = Field(ge=0)

class ProductResponse(BaseModel):
    id : int
    description : str
    price : float
    stock : int

    model_config = ConfigDict(from_attributes=True)