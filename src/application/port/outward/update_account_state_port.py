from abc import ABC, abstractmethod

from src.application.domain.entity.account import Account


class UpdateAccountStatePort(ABC):
    @abstractmethod
    async def update_activities(self, account: Account) -> None:
        pass
