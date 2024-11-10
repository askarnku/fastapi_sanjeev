"""adds content column

Revision ID: 3c7a3c210e29
Revises: f2985500482d
Create Date: 2024-11-09 18:34:27.054489

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3c7a3c210e29"
down_revision: Union[str, None] = "f2985500482d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
