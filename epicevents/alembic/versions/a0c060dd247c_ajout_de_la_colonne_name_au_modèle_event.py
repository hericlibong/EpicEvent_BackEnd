"""Ajout de la colonne name au modèle Event

Revision ID: a0c060dd247c
Revises: a657fa44eadf
Create Date: 2024-11-27 23:48:13.368247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0c060dd247c'
down_revision: Union[str, None] = 'a657fa44eadf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Ajoutez la colonne 'name' à la table 'events'
    op.add_column('events', sa.Column('name', sa.String(), nullable=True))


def downgrade():
    # Supprimez la colonne 'name' de la table 'events'
    op.drop_column('events', 'name')
