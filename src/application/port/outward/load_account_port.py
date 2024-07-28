from abc import ABC, abstractmethod
from datetime import datetime

from src.application.domain.entity.account import Account, AccountId


class LoadAccountPort(ABC):
    @abstractmethod
    def load_account(self, account_id: AccountId, baseline_date: datetime) -> Account:
        pass
