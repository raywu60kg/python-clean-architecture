from __future__ import annotations

from src.application.domain.entity.account import Account, AccountId
from src.application.domain.entity.activity_window import ActivityWindow
from src.application.domain.entity.money import Money
from tests.common.activity_test_builder import ActivityTestBuilder


class AccountTestBuilder:
    def __init__(self) -> None:
        self.__account_id = AccountId(42)
        self.__baseline_balance = Money(999)
        self.__activity_window = ActivityWindow([ActivityTestBuilder().build(), ActivityTestBuilder().build()])

    def with_account_id(self, account_id: AccountId) -> AccountTestBuilder:
        self.__account_id = account_id
        return self

    def with_baseline_balance(self, baseline_balance: Money) -> AccountTestBuilder:
        self.__baseline_balance = baseline_balance
        return self

    def with_activity_window(self, activity_window: ActivityWindow) -> AccountTestBuilder:
        self.__activity_window = activity_window
        return self

    def build(self) -> Account:
        return Account(self.__account_id, self.__baseline_balance, self.__activity_window)
