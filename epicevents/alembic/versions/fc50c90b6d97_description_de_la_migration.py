"""Description de la migration

Revision ID: fc50c90b6d97
Revises: 
Create Date: 2024-11-09 21:50:25.466085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc50c90b6d97'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('fullname', sa.String(), nullable=True))
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'department',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'role',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('GESTIONNAIRE', 'COMMERCIAL', 'SUPPORT', name='userrole'),
               existing_nullable=False, 
               postgresql_using="role::userrole")
    
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.alter_column('users', 'role',
               existing_type=sa.Enum('GESTIONNAIRE', 'COMMERCIAL', 'SUPPORT', name='userrole'),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.alter_column('users', 'department',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('users', 'fullname')
    # ### end Alembic commands ###