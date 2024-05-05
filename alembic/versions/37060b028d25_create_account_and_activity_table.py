"""create account and activity table

Revision ID: 37060b028d25
Revises:
Create Date: 2024-04-06 18:09:10.280214

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import DateTime, Integer

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "37060b028d25"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "account",
        sa.Column("id", Integer, primary_key=True),
    )

    op.create_table(
        "activity",
        sa.Column("id", Integer, primary_key=True),
        sa.Column("timestamp", DateTime(timezone=False)),
        sa.Column("owner_account_id", Integer, nullable=False),
        sa.Column("source_account_id", Integer, nullable=False),
        sa.Column("target_account_id", Integer, nullable=False),
        sa.Column("amount", Integer, nullable=False),
    )

    op.create_foreign_key(
        "fk/activity/owner_account_id/account/id",
        "activity",
        "account",
        ["owner_account_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk/activity/source_account_id/account/id",
        "activity",
        "account",
        ["source_account_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk/activity/target_account_id/account/id",
        "activity",
        "account",
        ["target_account_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk/activity/owner_account_id/account/id",
        "activity",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk/activity/source_account_id/account/id",
        "activity",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk/activity/target_account_id/account/id",
        "activity",
        type_="foreignkey",
    )

    op.drop_table("account")
    op.drop_table("activity")
