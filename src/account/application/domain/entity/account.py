from datetime import datetime

from pydantic import BaseModel

from .activity import Activity
from .activity_window import ActivityWindow
from .money import Money


class AccountId(BaseModel):
    value: int


class Account:
    def __init__(self, account_id: AccountId, baseline_balance: Money, activity_window: ActivityWindow) -> None:
        self.__account_id: AccountId = account_id
        self.__baseline_balance: Money = baseline_balance
        self.__activity_window: ActivityWindow = activity_window

    @property
    def account_id(self):
        return self.__account_id

    def calculate_balance(self) -> Money:
        return self.__baseline_balance + self.__activity_window.calculate_balance(self.__account_id)

    def withdraw(self, money: Money, target_account_id: AccountId) -> bool:
        if self.may_withdraw(money) is False:
            return False
        withdraw_activity: Activity = Activity(
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

    def deposit(self, money: Money, source_account_id: AccountId):
        deposit_activity: Activity = Activity(
            owner_account_id=self.account_id,
            source_account_id=source_account_id,
            target_account_id=self.account_id,
            timestamp=datetime.now(),
            money=money,
        )
        self.__activity_window.add_activity(deposit_activity)
        return True
