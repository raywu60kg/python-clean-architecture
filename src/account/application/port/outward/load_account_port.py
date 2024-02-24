from abc import ABC, abstractmethod
from datetime import datetime

from ...domain.entity.account import Account


class LoadAccountPort(ABC):
    @abstractmethod
    def load_account(self, account_id: str, baseline_date: datetime) -> Account:
        pass
