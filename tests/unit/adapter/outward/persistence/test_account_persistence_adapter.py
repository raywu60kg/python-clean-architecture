from datetime import datetime
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from src.adapter.outward.persistence.account_mapper import AccountMapper
from src.adapter.outward.persistence.account_persistence_adapter import AccountPersistenceAdapter
from src.adapter.outward.persistence.account_repository import AccountRepository
from src.adapter.outward.persistence.account_sqlalchemy_base import AccountSqlalchemyBase
from src.adapter.outward.persistence.activity_repository import ActivityRepository
from src.adapter.outward.persistence.activity_sqlalchemy_base import ActivitySqlalchemyBase
from src.application.domain.entity.account import AccountId
from src.application.domain.entity.activity_window import ActivityWindow
from src.application.domain.entity.money import Money
from tests.common.account_test_builder import AccountTestBuilder
from tests.common.activity_test_builder import ActivityTestBuilder


class TestAccountPersistenceAdapter(IsolatedAsyncioTestCase):
    async def test_loads_account(self) -> None:
        mock_account_repository = AsyncMock(spec=AccountRepository)
        mock_account_repository.get_by_id.return_value = AccountSqlalchemyBase(id=1)
        mock_activity_repository = AsyncMock(spec=ActivityRepository)
        mock_activity_repository.find_by_owner_since.return_value = [
            ActivitySqlalchemyBase(
                id=6,
                timestamp=datetime.strptime("2019-08-09 09:00:00.0", "%Y-%m-%d %H:%M:%S.%f"),
                owner_account_id=2,
                source_account_id=1,
                target_account_id=2,
                amount=1000,
            ),
            ActivitySqlalchemyBase(
                id=8,
                timestamp=datetime.strptime("2019-08-09 10:00:00.0", "%Y-%m-%d %H:%M:%S.%f"),
                owner_account_id=2,
                source_account_id=2,
                target_account_id=1,
                amount=1000,
            ),
        ]
        mock_activity_repository.get_withdrawal_balance_until.return_value = 500
        mock_activity_repository.get_deposit_balance_until.return_value = 1000
        account_persistence_adapter = AccountPersistenceAdapter(
            account_mapper=AccountMapper(),
            activity_repository=mock_activity_repository,
            account_repository=mock_account_repository,
        )
        account_id = AccountId(1)
        baseline_date = datetime(2018, 8, 10, 0, 0)

        account = await account_persistence_adapter.load_account(account_id, baseline_date)

        self.assertEqual(len(account.activity_window.activities), 2)
        self.assertEqual(account.calculate_balance(), Money(500))

    async def test_updates_activities(self) -> None:
        account = (
            AccountTestBuilder()
            .with_baseline_balance(Money(555))
            .with_activity_window(ActivityWindow([ActivityTestBuilder().with_money(Money(1)).build()]))
            .build()
        )

        mock_account_repository = AsyncMock(spec=AccountRepository)
        mock_activity_repository = AsyncMock(spec=ActivityRepository)
        mock_activity_repository.save.return_value = None
        account_persistence_adapter = AccountPersistenceAdapter(
            account_mapper=AccountMapper(),
            activity_repository=mock_activity_repository,
            account_repository=mock_account_repository,
        )
        await account_persistence_adapter.update_activities(account=account)
        self.assertEqual(mock_activity_repository.save.call_count, 1)
