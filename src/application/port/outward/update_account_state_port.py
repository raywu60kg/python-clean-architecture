from abc import ABC, abstractmethod

from ...domain.entity.account import Account


class UpdateAccountStatePort(ABC):
    @abstractmethod
    def update_activities(self, account: Account) -> None:
        pass
