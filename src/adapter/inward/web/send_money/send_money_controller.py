from fastapi import APIRouter, Path

from src.application.domain.entity.account import AccountId
from src.application.domain.entity.money import Money
from src.application.port.inward.send_money.send_money_command import SendMoneyCommand
from src.application.port.inward.send_money.send_money_use_case import SendMoneyUseCase

router = APIRouter()


@router.post("/accounts/send/{source_account_id}/{target_account_id}/{amount}")
async def send_money(
    send_money_use_case: SendMoneyUseCase,
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
