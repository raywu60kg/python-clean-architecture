from datetime import datetime, timedelta

from src.application.domain.entity.account import Account
from src.application.domain.service.send_money.money_transfer_properties import MoneyTransferProperties
from src.application.domain.service.send_money.send_money_account_not_found_exception import (
    SendMoneyAccountNotFoundException,
)
from src.application.domain.service.send_money.threshold_exceed_exception import ThresholdExceededException
from src.application.port.inward.send_money.send_money_command import SendMoneyCommand
from src.application.port.inward.send_money.send_money_use_case import SendMoneyUseCase
from src.application.port.outward.account_lock import AccountLock
from src.application.port.outward.load_account_port import LoadAccountPort
from src.application.port.outward.update_account_state_port import UpdateAccountStatePort


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

    async def send_money(self, command: SendMoneyCommand) -> bool:
        baseline_date: datetime = datetime.now() - timedelta(days=10)

        source_account: Account = await self.__load_account_port.load_account(
            account_id=command.source_account_id, baseline_date=baseline_date
        )
        target_account: Account = await self.__load_account_port.load_account(
            account_id=command.target_account_id, baseline_date=baseline_date
        )

        source_account_id = source_account.account_id
        target_account_id = target_account.account_id
        if source_account_id is None or target_account_id is None:
            raise SendMoneyAccountNotFoundException(from_account_id=source_account_id, to_account_id=target_account_id)

        self.__account_lock.lock_account(source_account_id)
        if source_account.withdraw(money=command.money, target_account_id=target_account_id) is False:
            self.__account_lock.release_account(source_account_id)
            return False

        self.__account_lock.lock_account(target_account_id)
        if target_account.deposit(money=command.money, source_account_id=source_account_id) is False:
            self.__account_lock.release_account(source_account_id)
            self.__account_lock.release_account(target_account_id)
            return False

        await self.__update_account_state_port.update_activities(source_account)
        await self.__update_account_state_port.update_activities(target_account)
        self.__account_lock.release_account(source_account_id)
        self.__account_lock.release_account(target_account_id)
        return True

    def check_threshold(self, command: SendMoneyCommand) -> None:
        if command.money.is_greater_than(self.__money_transfer_properties.maximum_transfer_threshold):
            raise ThresholdExceededException(self.__money_transfer_properties.maximum_transfer_threshold, command.money)
