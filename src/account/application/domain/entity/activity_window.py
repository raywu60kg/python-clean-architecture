from datetime import datetime
from typing import List, Optional

from money import Money

from .account import AccountId
from .activity import Activity


class ActivityWindow:
    def __init__(self, activities: List[Activity]) -> None:
        self.__activities: List[Activity] = activities

    @property
    def activities(self):
        return self.__activities

    def calculate_balance(self, account_id: AccountId):
        deposit_balance: Money = Money(0)
        withdrawal_balance: Money = Money(0)

        activity: Activity
        for activity in self.__activities:
            if activity.target_account_id == account_id:
                deposit_balance += activity.money
            if activity.source_account_id == account_id:
                withdrawal_balance += activity.money
        return deposit_balance - withdrawal_balance

    def get_start_time(self):
        first_activity_time: Optional[datetime] = None
        activity: Activity
        for activity in self.__activities:
            if first_activity_time is None:
                first_activity_time = activity.timestamp
            else:
                if activity.timestamp < first_activity_time:
                    first_activity_time = activity.timestamp
        return first_activity_time

    def get_end_time(self):
        latest_activity_time: Optional[datetime] = None
        activity: Activity
        for activity in self.__activities:
            if latest_activity_time is None:
                latest_activity_time = activity.timestamp
            else:
                if activity.timestamp > latest_activity_time:
                    latest_activity_time = activity.timestamp
        return latest_activity_time

    def add_activity(self, activity: Activity) -> None:
        self.activities.append(activity)
