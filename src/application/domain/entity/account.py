from datetime import datetime

from src.application.domain.entity.account_not_persisted_exception import AccountNotPersistedException
from src.application.domain.entity.activity import Activity
from src.application.domain.entity.activity_window import ActivityWindow
from src.application.domain.entity.money import Money


class AccountId:
    def __init__(self, value: int) -> None:
        self.__value = value

    @property
    def value(self) -> int:
        return self.__value


class Account:
    def __init__(self, account_id: AccountId | None, baseline_balance: Money, activity_window: ActivityWindow) -> None:
        self.__account_id = account_id
        self.__baseline_balance = baseline_balance
        self.__activity_window = activity_window

    @property
    def account_id(self) -> AccountId | None:
        return self.__account_id

    @property
    def activity_window(self) -> ActivityWindow:
        return self.__activity_window

    def calculate_balance(self) -> Money:
        if self.account_id is None:
            raise AccountNotPersistedException()
        return self.__baseline_balance + self.__activity_window.calculate_balance(self.account_id)  # type: ignore

    def withdraw(self, money: Money, target_account_id: AccountId) -> bool:
        if self.account_id is None:
            raise AccountNotPersistedException()
        if self.may_withdraw(money) is False:
            return False
        withdraw_activity = Activity(
            owner_account_id=self.account_id,
            source_account_id=self.account_id,
            target_account_id=target_account_id,
            timestamp=datetime.now(),
            money=money,
        )
        self.__activity_window.add_activity(withdraw_activity)
        return True

    def may_withdraw(self, money: Money) -> bool:
        balance_after_withdraw: Money = self.calculate_balance() - money
        return balance_after_withdraw.is_positive_or_zero()

    def deposit(self, money: Money, source_account_id: AccountId) -> bool:
        if self.account_id is None:
            raise AccountNotPersistedException()
        deposit_activity: Activity = Activity(
            owner_account_id=self.account_id,
            source_account_id=source_account_id,
            target_account_id=self.account_id,
            timestamp=datetime.now(),
            money=money,
        )
        self.__activity_window.add_activity(deposit_activity)
        return True
