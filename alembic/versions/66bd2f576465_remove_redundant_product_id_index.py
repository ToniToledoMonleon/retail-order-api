"""remove redundant product id index

Revision ID: 66bd2f576465
Revises: faad7dcb2fce
Create Date: 2026-09-10 15:22:04.178777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66bd2f576465'
down_revision: Union[str, Sequence[str], None] = 'faad7dcb2fce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(
        "ix_products_id",
        table_name="products",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.create_index(
        "ix_products_id",
        "products",
        ["id"],
        unique=False,
    )
