"""add_owner_id_and_image_url

Revision ID: b3b80ba6de19
Revises: 
Create Date: 2026-10-25 13:30:25.060114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3b80ba6de19'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Это просто колонка в БД — неважно, что в модели она часть relationship
    op.add_column('comics', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('comics', sa.Column('image_url', sa.String(), nullable=True))

    # Если хочешь сразу сделать внешний ключ (чтобы БД знала про связь)
    op.create_foreign_key(
        'fkey_comics_owner_id',
        'comics', 'users',
        ['owner_id'], ['id']
    )


def downgrade() -> None:
    # Удаляем колонки в обратном порядке
    op.drop_index(op.f('ix_comics_owner_id'), table_name='comics')
    op.drop_column('comics', 'image_url')
    op.drop_column('comics', 'owner_id')
