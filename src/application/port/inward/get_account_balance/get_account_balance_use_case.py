from abc import ABC, abstractmethod

from src.application.domain.entity.money import Money
from src.application.port.inward.get_account_balance.get_account_balance_query import GetAccountBalanceQuery


class GetAccountBalanceUseCase(ABC):
    @abstractmethod
    async def get_account_balance(self, query: GetAccountBalanceQuery) -> Money:
        pass
