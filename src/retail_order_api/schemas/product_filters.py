from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class ProductFilters(BaseModel):
    limit: int = Field(default=20,ge=1,le=100,)
    offset: int = Field(default=0,ge=0,)
    active: bool | None = None
    min_price: Decimal | None = Field(default=None,ge=0,)
    max_price: Decimal | None = Field(default=None,ge=0,)
    search: str | None = Field(default=None,min_length=1,max_length=100,)
    sort_by: Literal[
        "id",
        "price",
        "stock",
        "created_at",
    ] = "id"

    sort_order: Literal[
        "asc",
        "desc",
    ] = "asc"

    @model_validator(mode="after")
    def validate_price_range(self):
        if (
            self.min_price is not None
            and self.max_price is not None
            and self.min_price > self.max_price
        ):
            raise ValueError(
                "min_price cannot be greater than max_price"
            )

        return self