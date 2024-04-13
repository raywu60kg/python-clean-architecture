from datetime import datetime, timedelta

from ....port.inward.send_money.send_money_command import SendMoneyCommand
from ....port.inward.send_money.send_money_use_case import SendMoneyUseCase
from ....port.outward.account_lock import AccountLock
from ....port.outward.load_account_port import LoadAccountPort
from ....port.outward.update_account_state_port import UpdateAccountStatePort
from ...entity.account import Account, AccountId
from .money_transfer_properties import MoneyTransferProperties
from .threshold_exceed_exception import ThresholdExceededException


class SendMoneyService(SendMoneyUseCase):
    def __init__(
        self,
        load_account_port: LoadAccountPort,
        account_lock: AccountLock,
        update_account_state_port: UpdateAccountStatePort,
        money_transfer_properties: MoneyTransferProperties,
    ) -> None:
        self.__load_account_port: LoadAccountPort = load_account_port
        self.__account_lock: AccountLock = account_lock
        self.__update_account_state_port: UpdateAccountStatePort = update_account_state_port
        self.__money_transfer_properties: MoneyTransferProperties = money_transfer_properties

    def send_money(self, command: SendMoneyCommand):
        baseline_date: datetime = datetime.now() - timedelta(days=10)

        source_account: Account = self.__load_account_port.load_account(
            account_id=command.source_account_id, baseline_date=baseline_date
        )

        target_account: Account = self.__load_account_port.load_account(
            account_id=command.target_account_id, baseline_date=baseline_date
        )

        source_account_id: AccountId = source_account.account_id
        target_account_id: AccountId = target_account.account_id

        self.__account_lock.lock_account(source_account_id)
        if source_account.withdraw(money=command.money, target_account_id=target_account_id) is False:
            self.__account_lock.release_account(source_account_id)
            return False

        self.__account_lock.lock_account(target_account_id)
        if target_account.deposit(money=command.money, source_account_id=source_account_id) is False:
            self.__account_lock.release_account(account_id=source_account_id)
            self.__account_lock.release_account(account_id=target_account_id)
            return False

        self.__update_account_state_port.update_activities(source_account)
        self.__update_account_state_port.update_activities(target_account)
        return True

    def check_threshold(self, command: SendMoneyCommand):
        if command.money.is_greater_than(self.__money_transfer_properties.maximum_transfer_threshold):
            raise ThresholdExceededException(self.__money_transfer_properties.maximum_transfer_threshold, command.money)
