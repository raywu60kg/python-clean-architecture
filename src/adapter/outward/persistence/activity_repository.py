from datetime import datetime
from typing import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapter.outward.persistence.activity_sqlalchemy_base import ActivitySqlalchemyBase


class ActivityRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]):
        self.__session_factory = session_factory

    async def find_by_owner_since(self, owner_account_id: int, since: datetime) -> list[ActivitySqlalchemyBase]:
        async with self.__session_factory() as session:
            res = await session.execute(
                select(ActivitySqlalchemyBase).where(
                    ActivitySqlalchemyBase.owner_account_id == owner_account_id,
                    ActivitySqlalchemyBase.timestamp >= since,
                )
            )
            activity_sqlalchemy_base_sequence = res.scalars().all()
            return list(activity_sqlalchemy_base_sequence)

    async def get_deposit_balance_until(self, account_id: int, until: datetime) -> int | None:
        async with self.__session_factory() as session:
            res = await session.execute(
                select(func.sum(ActivitySqlalchemyBase.amount)).filter(
                    ActivitySqlalchemyBase.target_account_id == account_id,
                    ActivitySqlalchemyBase.owner_account_id == account_id,
                    ActivitySqlalchemyBase.timestamp < until,
                )
            )
            deposit_balance = res.scalar()
            if deposit_balance is None:
                return None

            return deposit_balance

    async def get_withdrawal_balance_until(self, account_id: int, until: datetime) -> int | None:
        async with self.__session_factory() as session:
            res = await session.execute(
                select(func.sum(ActivitySqlalchemyBase.amount)).filter(
                    ActivitySqlalchemyBase.source_account_id == account_id,
                    ActivitySqlalchemyBase.owner_account_id == account_id,
                    ActivitySqlalchemyBase.timestamp < until,
                )
            )
            withdrawal_balance = res.scalar()
            if withdrawal_balance is None:
                return None

            return withdrawal_balance

    async def save(self, activity: ActivitySqlalchemyBase) -> None:
        async with self.__session_factory() as session:
            session.add(activity)
            await session.commit()
