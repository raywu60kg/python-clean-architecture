from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from httpx import AsyncClient

from src.application.domain.entity.account import AccountId
from src.application.domain.entity.money import Money
from src.application.port.inward.send_money.send_money_command import SendMoneyCommand
from src.application.port.inward.send_money.send_money_use_case import SendMoneyUseCase
from src.main import app


class TestSendMoneyController(IsolatedAsyncioTestCase):
    async def test_send_money(self) -> None:
        send_money_use_case_mock = AsyncMock(spec=SendMoneyUseCase)
        send_money_use_case_mock.send_money.return_value = True

        with app.state.container.send_money_service.override(send_money_use_case_mock):
            async with AsyncClient(app=app, base_url="http://testserver") as client:
                response = await client.post(f"/accounts/send/{41}/{42}/{500}")
                assert response.status_code == 200
        send_money_use_case_mock.send_money.assert_called_once_with(
            command=SendMoneyCommand(source_account_id=AccountId(41), target_account_id=AccountId(42), money=Money(500))
        )
