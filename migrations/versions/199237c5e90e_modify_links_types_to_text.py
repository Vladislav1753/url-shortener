"""modify links types to text

Revision ID: 199237c5e90e
Revises: 0c9b9b641049
Create Date: 2026-06-27 13:23:26.444750

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "199237c5e90e"
down_revision: Union[str, Sequence[str], None] = "0c9b9b641049"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "links",
        "code",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.Text(),
        existing_nullable=False,
    )
    op.alter_column(
        "links",
        "original_url",
        existing_type=sa.VARCHAR(length=2048),
        type_=sa.Text(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "links",
        "original_url",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(length=2048),
        existing_nullable=False,
    )
    op.alter_column(
        "links",
        "code",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
