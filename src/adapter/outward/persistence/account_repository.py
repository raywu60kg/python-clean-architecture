from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapter.outward.persistence.account_not_found_exception import AccountNotFoundException
from src.adapter.outward.persistence.account_sqlalchemy_base import AccountSqlalchemyBase


class AccountRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]):
        self.__session_factory = session_factory

    async def get_by_id(self, account_id: int) -> AccountSqlalchemyBase:
        async with self.__session_factory() as session:
            res = await session.execute(select(AccountSqlalchemyBase).filter(AccountSqlalchemyBase.id == account_id))
            account_sqlalchemy_base = res.scalar()
            if not account_sqlalchemy_base:
                raise AccountNotFoundException(account_id=account_id)
            return account_sqlalchemy_base
