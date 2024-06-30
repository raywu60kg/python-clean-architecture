from datetime import datetime
from typing import List, Optional

from money import Money

from .account import AccountId
from .activity import Activity


class ActivityWindow:
    def __init__(self, activities: List[Activity]) -> None:
        self.__activities = activities

    @property
    def activities(self) -> List[Activity]:
        return self.__activities

    def calculate_balance(self, account_id: Optional[AccountId]) -> Money:
        deposit_balance: Money = Money(0)
        withdrawal_balance: Money = Money(0)

        activity: Activity
        for activity in self.__activities:
            if activity.target_account_id == account_id:
                deposit_balance += activity.money
            if activity.source_account_id == account_id:
                withdrawal_balance += activity.money
        return deposit_balance - withdrawal_balance

    def get_start_time(self) -> datetime:
        return min(self.__activities, key=lambda x: x.timestamp).timestamp

    def get_end_time(self):
        return max(self.__activities, key=lambda x: x.timestamp).timestamp

    def add_activity(self, activity: Activity) -> None:
        self.activities.append(activity)
