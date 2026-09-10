"""constraint to price and stock

Revision ID: b2f755a4e3fd
Revises: 81e44662ad36
Create Date: 2026-09-10 09:04:38.898022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2f755a4e3fd'
down_revision: Union[str, Sequence[str], None] = '81e44662ad36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint(
        "ck_products_price_positive",
        "products",
        "price > 0",
    )

    op.create_check_constraint(
        "ck_products_stock_non_negative",
        "products",
        "stock >= 0",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("ck_products_price_positive", "products", type_="check")
    op.drop_constraint("ck_products_stock_non_negative", "products", type_="check")
