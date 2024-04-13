from pydantic import BaseModel, field_validator

from ....domain.entity.account import AccountId
from ....domain.entity.money import Money


class SendMoneyCommand(BaseModel):
    source_account_id: AccountId
    target_account_id: AccountId
    money: Money

    @field_validator("Money")
    @classmethod
    def money_must_be_positive(cls, money: Money) -> Money:
        if money.is_greater_than(Money(0)):
            raise ValueError(f"Amount has to be positive but got {money}")
        return money
