from decimal import Decimal

from sqlalchemy import CheckConstraint, Index, Integer, Numeric, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from retail_order_api.db.database import Base



class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint(
            "price > 0",
            name="ck_products_price_positive",
        ),
        CheckConstraint(
            "stock >= 0",
            name="ck_products_stock_non_negative",
        ),
        Index(
            "ix_products_description_trgm",
            "description",
            postgresql_using="gin",
            postgresql_ops={
                "description": "gin_trgm_ops",
            },
        ),
        Index(
            "ix_products_sku_trgm",
            "sku",
            postgresql_using="gin",
            postgresql_ops={
                "sku": "gin_trgm_ops",
            },
        ),
    )
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )