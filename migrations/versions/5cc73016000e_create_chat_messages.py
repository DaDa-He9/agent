"""create chat messages

Revision ID: 5cc73016000e
Revises:
Create Date: 2026-10-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5cc73016000e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """创建聊天记录表。"""
    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(length=100), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default="received",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_chat_messages_user_id",
        "chat_messages",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """删除聊天记录表。"""
    op.drop_index(
        "ix_chat_messages_user_id",
        table_name="chat_messages",
    )
    op.drop_table("chat_messages")