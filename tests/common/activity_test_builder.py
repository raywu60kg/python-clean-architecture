from __future__ import annotations

from datetime import datetime

from src.application.domain.entity.account import AccountId
from src.application.domain.entity.activity import Activity, ActivityId
from src.application.domain.entity.money import Money


class ActivityTestBuilder:
    def __init__(self) -> None:
        self.__activity_id: ActivityId | None = None
        self.__owner_account_id = AccountId(42)
        self.__source_account_id = AccountId(42)
        self.__target_account_id = AccountId(41)
        self.__timestamp = datetime(2024, 1, 1)
        self.__money = Money(999)

    def with_activity_id(self, activity_id: ActivityId) -> ActivityTestBuilder:
        self.__activity_id = activity_id
        return self

    def with_owner_account(self, account_id: AccountId) -> ActivityTestBuilder:
        self.__owner_account_id = account_id
        return self

    def with_source_account(self, account_id: AccountId) -> ActivityTestBuilder:
        self.__source_account_id = account_id
        return self

    def with_target_account(self, account_id: AccountId) -> ActivityTestBuilder:
        self.__target_account_id = account_id
        return self

    def with_timestamp(self, timestamp: datetime) -> ActivityTestBuilder:
        self.__timestamp = timestamp
        return self

    def with_money(self, money: Money) -> ActivityTestBuilder:
        self.money = money
        return self

    def build(self) -> Activity:
        return Activity(
            activity_id=self.__activity_id,
            owner_account_id=self.__owner_account_id,
            source_account_id=self.__source_account_id,
            target_account_id=self.__target_account_id,
            timestamp=self.__timestamp,
            money=self.__money,
        )
