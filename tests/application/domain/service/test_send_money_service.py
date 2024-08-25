from datetime import datetime
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, call

from src.application.domain.entity.account import Account, AccountId
from src.application.domain.entity.money import Money
from src.application.domain.service.send_money.money_transfer_properties import MoneyTransferProperties
from src.application.domain.service.send_money.send_money_service import SendMoneyService
from src.application.port.inward.send_money.send_money_command import SendMoneyCommand
from src.application.port.outward.account_lock import AccountLock
from src.application.port.outward.load_account_port import LoadAccountPort
from src.application.port.outward.update_account_state_port import UpdateAccountStatePort


class TestSendMoneyService(IsolatedAsyncioTestCase):
    load_account_port = Mock(spec=LoadAccountPort)
    account_lock = Mock(spec=AccountLock)
    update_account_state_port = Mock(spec=UpdateAccountStatePort)
    money_transfer_properties = MoneyTransferProperties()
    send_money_service = SendMoneyService(
        load_account_port=load_account_port,
        account_lock=account_lock,
        update_account_state_port=update_account_state_port,
        money_transfer_properties=money_transfer_properties,
    )

    async def test_given_withdrawal_fails_then_only_source_account_is_locked_and_released(self) -> None:
        source_account_id = AccountId(41)
        source_account = Mock(spec=Account)
        source_account.account_id = source_account_id
        source_account.withdraw.return_value = False

        target_account_id = AccountId(42)
        target_account = Mock(spec=Account)
        target_account.account_id = target_account_id
        target_account.deposit.return_value = True

        async def load_account_port_side_effect(account_id: AccountId, baseline_date: datetime) -> Mock | None:
            return_value_map = {
                AccountId(41): source_account,
                AccountId(42): target_account,
            }
            return return_value_map.get(account_id)

        self.load_account_port.load_account = AsyncMock(side_effect=load_account_port_side_effect)
        command = SendMoneyCommand(source_account_id, target_account_id, Money(300))

        success = await self.send_money_service.send_money(command)
        self.assertFalse(success)

        self.account_lock.lock_account.assert_called_once_with(source_account_id)
        self.account_lock.release_account.assert_called_once_with(source_account_id)
        assert call(target_account_id) not in self.account_lock.lock_account.mock_calls

    async def test_transaction_succeeds(self) -> None:
        source_account_id = AccountId(41)
        source_account = Mock(spec=Account)
        source_account.account_id = source_account_id
        source_account.withdraw.return_value = True

        target_account_id = AccountId(42)
        target_account = Mock(spec=Account)
        target_account.account_id = target_account_id
        target_account.deposit.return_value = True

        async def load_account_port_side_effect(account_id: AccountId, baseline_date: datetime) -> Mock | None:
            return_value_map = {
                AccountId(41): source_account,
                AccountId(42): target_account,
            }
            return return_value_map.get(account_id)

        self.load_account_port.load_account = AsyncMock(side_effect=load_account_port_side_effect)

        money = Money(500)

        command = SendMoneyCommand(source_account.account_id, target_account.account_id, money)

        success = await self.send_money_service.send_money(command)
        self.assertTrue(success)

        source_account_id = source_account.account_id
        target_account_id = target_account.account_id
        self.account_lock.lock_account.assert_has_calls([call(source_account_id), call(target_account_id)])
        source_account.withdraw.assert_called_once_with(money=money, target_account_id=target_account_id)
        self.account_lock.release_account.assert_has_calls([call(source_account_id), call(target_account_id)])

        target_account.deposit.assert_called_once_with(money=money, source_account_id=source_account_id)

        self.then_accounts_have_been_updated([source_account_id, target_account_id])

    def then_accounts_have_been_updated(self, account_ids: list[AccountId]) -> None:
        account_captor = self.update_account_state_port.update_activities.mock_calls
        updated_account_ids = [arg_call.args[0].account_id for arg_call in account_captor]

        for account_id in account_ids:
            self.assertIn(account_id, updated_account_ids)
