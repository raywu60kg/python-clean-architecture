from pydantic import BaseModel

from ...entity.money import Money


class MoneyTransferProperties(BaseModel):
    maximum_transfer_threshold: Money = Money(1_000_000)
