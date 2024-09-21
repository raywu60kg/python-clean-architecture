"""add data for demo

Revision ID: 8692f3902e1c
Revises: 25890a85f01f
Create Date: 2024-09-21 19:36:39.396840

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8692f3902e1c"
down_revision: Union[str, None] = "25890a85f01f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    conn.execute(sa.text("INSERT INTO account (id) VALUES (1)"))
    conn.execute(sa.text("INSERT INTO account (id) VALUES (2)"))

    activities = [
        (1001, "2018-08-08 08:00:00", 1, 1, 2, 500),
        (1002, "2018-08-08 08:00:00", 2, 1, 2, 500),
        (1003, "2018-08-09 10:00:00", 1, 2, 1, 1000),
        (1004, "2018-08-09 10:00:00", 2, 2, 1, 1000),
        (1005, "2019-08-09 09:00:00", 1, 1, 2, 1000),
        (1006, "2019-08-09 09:00:00", 2, 1, 2, 1000),
        (1007, "2019-08-09 10:00:00", 1, 2, 1, 1000),
        (1008, "2019-08-09 10:00:00", 2, 2, 1, 1000),
    ]

    for activity in activities:
        conn.execute(
            sa.text("""
                INSERT INTO activity (id, timestamp, owner_account_id, source_account_id, target_account_id, amount)
                VALUES (:id, :timestamp, :owner_account_id, :source_account_id, :target_account_id, :amount)
            """),
            {
                "id": activity[0],
                "timestamp": activity[1],
                "owner_account_id": activity[2],
                "source_account_id": activity[3],
                "target_account_id": activity[4],
                "amount": activity[5],
            },
        )


def downgrade() -> None:
    conn = op.get_bind()

    conn.execute(sa.text("DELETE FROM activity WHERE id BETWEEN 1001 AND 1008"))

    conn.execute(sa.text("DELETE FROM account WHERE id IN (1, 2)"))
