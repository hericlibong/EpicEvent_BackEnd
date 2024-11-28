"""Rendre la colonne 'name' non nullable dans le modèle Event

Revision ID: 4c73a6435c36
Revises: a0c060dd247c
Create Date: 2024-11-28 00:59:13.615921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c73a6435c36'
down_revision: Union[str, None] = 'a0c060dd247c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('events', 'name', 
                    existing_type=sa.String(), 
                    nullable=False)


def downgrade() -> None:
    op.alter_column('events', 'name', 
                    existing_type=sa.String(), 
                    nullable=True)
