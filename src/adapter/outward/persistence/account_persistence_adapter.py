from datetime import datetime

from src.adapter.outward.persistence.account_mapper import AccountMapper
from src.adapter.outward.persistence.account_repository import AccountRepository
from src.adapter.outward.persistence.activity_repository import ActivityRepository
from src.application.domain.entity.account import Account, AccountId
from src.application.port.outward.load_account_port import LoadAccountPort
from src.application.port.outward.update_account_state_port import UpdateAccountStatePort


class AccountPersistenceAdapter(LoadAccountPort, UpdateAccountStatePort):
    def __init__(
        self,
        account_mapper: AccountMapper,
        activity_repository: ActivityRepository,
        account_repository: AccountRepository,
    ) -> None:
        self.__account_mapper = account_mapper
        self.__activity_repository = activity_repository
        self.__account_repository = account_repository

    async def load_account(self, account_id: AccountId, baseline_date: datetime) -> Account:
        account = await self.__account_repository.get_by_id(account_id=account_id.value)
        activities = await self.__activity_repository.find_by_owner_since(
            owner_account_id=account_id.value, since=baseline_date
        )
        withdrawal_balance = (
            await self.__activity_repository.get_withdrawal_balance_until(account_id.value, baseline_date) or 0
        )
        deposit_balance = (
            await self.__activity_repository.get_deposit_balance_until(account_id.value, baseline_date) or 0
        )
        return self.__account_mapper.map_to_account(
            account_sqlalchemy_base=account,
            activities=activities,
            withdrawal_balance=withdrawal_balance,
            deposit_balance=deposit_balance,
        )

    async def update_activities(self, account: Account) -> None:
        for activity in account.activity_window.activities:
            if activity.activity_id is None:
                await self.__activity_repository.save(self.__account_mapper.map_to_activity_sqlalchemy_base(activity))
