from pydantic import BaseModel, field_validator

from ....domain.entity.account import AccountId
from ....domain.entity.money import Money


class SendMoneyCommand(BaseModel):
    source_account_id: AccountId
    target_account_id: AccountId
    money: Money

    @field_validator("name")
    @classmethod
    def money_must_be_positive(cls, v: str) -> str:
        if " " not in v:
            raise ValueError("must contain a space")
        return v.title()

    # @amount.setter
    # def amount(self, value: float):
    #     if value < 0:
    #         raise ValueError(f"Amount has to be positive but got {value}")
    #     self.__amount = value
