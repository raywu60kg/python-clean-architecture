from datetime import datetime

from .activity import Activity
from .activity_window import ActivityWindow


class Account:
    def __init__(self, account_id: str, baseline_balance: float, activity_window: ActivityWindow) -> None:
        self.__account_id = account_id
        self.__baseline_balance = baseline_balance
        self.__activity_window = activity_window

    @property
    def account_id(self):
        return self.__account_id

    def calculate_balance(self) -> float:
        return self.__baseline_balance + self.__activity_window.calculate_balance(self.__account_id)

    def withdraw(self, amount: float, target_account_id: str) -> bool:
        if self.may_withdraw(amount) is False:
            return False
        withdraw_activity: Activity = Activity(
            owner_account_id=self.account_id,
            source_account_id=self.account_id,
            target_account_id=target_account_id,
            timestamp=datetime.now(),
            amount=amount,
        )
        self.__activity_window.add_activity(withdraw_activity)
        return True

    def may_withdraw(self, amount: float) -> bool:
        return self.calculate_balance() - amount >= 0

    def deposit(self, amount: float, source_account_id: str):
        deposit_activity: Activity = Activity(
            owner_account_id=self.account_id,
            source_account_id=source_account_id,
            target_account_id=self.account_id,
            timestamp=datetime.now(),
            amount=amount,
        )
        self.__activity_window.add_activity(deposit_activity)
        return True
