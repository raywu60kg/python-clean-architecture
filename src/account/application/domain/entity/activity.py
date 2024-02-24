from datetime import datetime
from typing import Optional


class Activity:
    def __init__(
        self, owner_account_id: str, source_account_id: str, target_account_id: str, timestamp: datetime, amount: float
    ) -> None:
        self.__id: Optional[str] = None
        self.__owner_account_id: str = owner_account_id
        self.__source_account_id: str = source_account_id
        self.__target_account_id: str = target_account_id
        self.__timestamp: datetime = timestamp
        self.__amount: float = amount

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @property
    def target_account_id(self) -> str:
        return self.__target_account_id

    @property
    def source_account_id(self) -> str:
        return self.__source_account_id

    @property
    def amount(self) -> float:
        return self.__amount
