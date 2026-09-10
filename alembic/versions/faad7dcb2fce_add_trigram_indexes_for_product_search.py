"""add trigram indexes for product search

Revision ID: faad7dcb2fce
Revises: b2f755a4e3fd
Create Date: 2026-09-10 15:11:00.548449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'faad7dcb2fce'
down_revision: Union[str, Sequence[str], None] = 'b2f755a4e3fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "CREATE EXTENSION IF NOT EXISTS pg_trgm"
    )

    op.create_index(
        "ix_products_description_trgm",
        "products",
        ["description"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={
            "description": "gin_trgm_ops",
        },
    )

    op.create_index(
        "ix_products_sku_trgm",
        "products",
        ["sku"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={
            "sku": "gin_trgm_ops",
        },
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_products_description_trgm", table_name="products")
    op.drop_index("ix_products_sku_trgm", table_name="products")
