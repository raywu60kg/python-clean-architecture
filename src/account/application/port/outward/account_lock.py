from abc import ABC, abstractmethod


class AccountLock(ABC):
    @abstractmethod
    def lock_account(self, account_id: str):
        pass

    @abstractmethod
    def release_account(self, account_id: str):
        pass
