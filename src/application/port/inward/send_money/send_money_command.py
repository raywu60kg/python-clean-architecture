from src.application.domain.entity.account import AccountId
from src.application.domain.entity.money import Money
from src.application.port.inward.send_money.send_money_negative_exception import SendMoneyNegativeException


class SendMoneyCommand:
    def __init__(self, source_account_id: AccountId, target_account_id: AccountId, money: Money):
        self.__source_account_id = source_account_id
        self.__target_account_id = target_account_id
        self.money = money

    @property
    def money(self) -> Money:
        return self.__money

    @money.setter
    def money(self, money: Money) -> None:
        if money.is_greater_than(Money(0)):
            raise SendMoneyNegativeException(money=money)
        self.__money = money

    @property
    def source_account_id(self) -> AccountId:
        return self.__source_account_id

    @property
    def target_account_id(self) -> AccountId:
        return self.__target_account_id
