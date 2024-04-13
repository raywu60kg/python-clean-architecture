from pydantic import BaseModel

from ....domain.entity.account import AccountId


class GetAccountBalanceQuery(BaseModel):
    account_id: AccountId
