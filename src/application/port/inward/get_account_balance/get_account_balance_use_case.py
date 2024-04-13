from abc import ABC, abstractmethod

from .get_account_balance_query import GetAccountBalanceQuery


class GetAccountBalanceUseCase(ABC):
    @abstractmethod
    def get_account_balance(self, query: GetAccountBalanceQuery):
        pass
