from fastapi import APIRouter, Path

from src.application.domain.entity.account import AccountId
from src.application.port.inward.get_account_balance.get_account_balance_query import GetAccountBalanceQuery
from src.application.port.inward.get_account_balance.get_account_balance_use_case import GetAccountBalanceUseCase

router = APIRouter()


@router.get("/accounts/balance/{owner_account_id}/")
async def get_account_balance(
    get_account_balance_use_case: GetAccountBalanceUseCase,
    owner_account_id: int = Path(..., description="The ID of the owner account"),
) -> int:
    query = GetAccountBalanceQuery(account_id=AccountId(value=owner_account_id))
    balance = await get_account_balance_use_case.get_account_balance(query=query)
    return balance.amount
