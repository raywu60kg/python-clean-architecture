from unittest import TestCase
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.application.domain.entity.account import AccountId
from src.application.domain.entity.money import Money
from src.application.domain.service.send_money.send_money_service import SendMoneyService
from src.application.port.inward.send_money.send_money_command import SendMoneyCommand
from src.main import app


class TestSendMoneyController(TestCase):
    @pytest.fixture(autouse=True)
    def request_fixture(self, client: TestClient) -> None:
        self.client = client

    def test_send_money(self) -> None:
        send_money_use_case_mock = AsyncMock(spec=SendMoneyService)
        send_money_use_case_mock.send_money.return_value = True

        with app.state.container.send_money_service.override(send_money_use_case_mock):
            response = self.client.post(f"/accounts/send/{41}/{42}/{500}")
            assert response.status_code == 200
        send_money_use_case_mock.send_money.assert_called_once_with(
            command=SendMoneyCommand(source_account_id=AccountId(41), target_account_id=AccountId(42), money=Money(500))
        )
