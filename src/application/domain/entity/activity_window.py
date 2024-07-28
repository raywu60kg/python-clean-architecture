from datetime import datetime

from src.application.domain.entity.account import AccountId
from src.application.domain.entity.activity import Activity
from src.application.domain.entity.money import Money


class ActivityWindow:
    def __init__(self, activities: list[Activity]) -> None:
        self.__activities = activities

    @property
    def activities(self) -> list[Activity]:
        return self.__activities

    def calculate_balance(self, account_id: AccountId) -> Money:
        deposit_balance: Money = Money(0)
        withdrawal_balance: Money = Money(0)

        for activity in self.__activities:
            if activity.target_account_id == account_id:
                deposit_balance += activity.money
            if activity.source_account_id == account_id:
                withdrawal_balance += activity.money
        return deposit_balance - withdrawal_balance

    def get_start_time(self) -> datetime:
        return min(self.__activities, key=lambda x: x.timestamp).timestamp

    def get_end_time(self) -> datetime:
        return max(self.__activities, key=lambda x: x.timestamp).timestamp

    def add_activity(self, activity: Activity) -> None:
        self.activities.append(activity)
