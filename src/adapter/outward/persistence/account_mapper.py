from typing import List

from ....application.domain.entity.account import Account, AccountId
from ....application.domain.entity.activity import Activity, ActivityId
from ....application.domain.entity.activity_window import ActivityWindow
from ....application.domain.entity.money import Money
from .account_sqlalchemy_base import AccountSqlalchemyBase
from .activity_sqlalchemy_base import ActivitySqlalchemyBase


class AccountMapper:
    def map_to_account(
        self,
        account_sqlalchemy_base: AccountSqlalchemyBase,
        activities: List[ActivitySqlalchemyBase],
        withdrawal_balance: int,
        deposit_balance: int,
    ) -> Account:
        baseline_balance: Money = Money(deposit_balance) - Money(withdrawal_balance)
        return Account(
            account_id=AccountId(value=account_sqlalchemy_base.id),
            baseline_balance=baseline_balance,
            activity_window=self.map_to_activities_window(activities),
        )

    def map_to_activities_window(self, activities: List[ActivitySqlalchemyBase]) -> ActivityWindow:
        mapped_activities: List[Activity] = []
        for activity in activities:
            mapped_activities.append(
                Activity(
                    activity_id=ActivityId(value=activity.id),
                    owner_account_id=AccountId(value=activity.owner_account_id),
                    source_account_id=AccountId(value=activity.source_account_id),
                    target_account_id=AccountId(value=activity.target_account_id),
                    timestamp=activity.timestamp,
                    money=Money(value=activity.amount),
                )
            )
        return ActivityWindow(activities=mapped_activities)

    def map_to_activity_sqlalchemy_base(self, activity: Activity) -> ActivitySqlalchemyBase:
        return ActivitySqlalchemyBase(
            id=activity.activity_id.value if activity.activity_id is not None else None,
            timestamp=activity.timestamp,
            owner_account_id=activity.owner_account_id.value,  # type: ignore
            source_account_id=activity.source_account_id.value,  # type: ignore
            target_account_id=activity.target_account_id.value,  # type: ignore
            amount=activity.money.amount,
        )
