from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from src.application.domain.entity.account import AccountId
from src.application.domain.entity.money import Money
from src.application.port.inward.get_account_balance.get_account_balance_query import GetAccountBalanceQuery
from src.application.port.inward.get_account_balance.get_account_balance_use_case import GetAccountBalanceUseCase
from src.application.port.inward.send_money.send_money_command import SendMoneyCommand
from src.application.port.inward.send_money.send_money_use_case import SendMoneyUseCase
from src.common.container import Container

router = APIRouter()


@router.get("/accounts/balance/{owner_account_id}/")
@inject
async def get_account_balance(
    get_account_balance_use_case: GetAccountBalanceUseCase = Depends(Provide[Container.get_account_balance_service]),
    owner_account_id: int = Path(..., description="The ID of the owner account"),
) -> int:
    query = GetAccountBalanceQuery(account_id=AccountId(value=owner_account_id))
    balance = await get_account_balance_use_case.get_account_balance(query=query)
    return balance.amount


@router.post("/accounts/send/{source_account_id}/{target_account_id}/{amount}")
async def send_money(
    send_money_use_case: SendMoneyUseCase = Depends(Provide[Container.send_money_service]),
    source_account_id: int = Path(..., description="The ID of the source account"),
    target_account_id: int = Path(..., description="The ID of the target account"),
    amount: int = Path(..., description="The amount of money to send"),
) -> None:
    command = SendMoneyCommand(
        source_account_id=AccountId(value=source_account_id),
        target_account_id=AccountId(value=target_account_id),
        money=Money(value=amount),
    )
    await send_money_use_case.send_money(command=command)
    return
