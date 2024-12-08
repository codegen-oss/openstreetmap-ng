"""Add usage_count to user_token_email_reply

Revision ID: 175e464cf823
Revises: fdac1daabf02
Create Date: 2024-12-08 12:47:41.182418+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '175e464cf823'
down_revision: str | None = 'fdac1daabf02'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('note_comment_event_user_idx', table_name='note_comment')
    op.create_index('note_comment_event_user_id_idx', 'note_comment', ['event', 'user_id', 'id'], unique=False)
    op.add_column(
        'user_block',
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('statement_timestamp()'),
            nullable=False,
        ),
    )
    op.add_column(
        'user_token_email_reply', sa.Column('usage_count', sa.SmallInteger(), server_default='0', nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None: ...
