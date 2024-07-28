from abc import ABC, abstractmethod

from src.application.domain.entity.account import AccountId


class AccountLock(ABC):
    @abstractmethod
    def lock_account(self, account_id: AccountId) -> None:
        pass

    @abstractmethod
    def release_account(self, account_id: AccountId) -> None:
        pass
