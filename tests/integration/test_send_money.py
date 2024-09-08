from unittest import IsolatedAsyncioTestCase

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from src.application.domain.entity.account import AccountId
from src.application.domain.entity.money import Money
from src.common.container import Container


class SendMoneySystemTest(IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def request_fixture(self, client: TestClient) -> None:
        self.client = client

    async def test_send_money(self) -> None:
        # await self.init_test_db()

        source_account_id = AccountId(1)
        target_account_id = AccountId(2)
        transfer_amount = Money(500)

        initial_source_balance = self.client.get(f"/accounts/balance/{source_account_id.value}").json()
        initial_target_balance = self.client.get(f"/accounts/balance/{target_account_id.value}").json()

        response = self.client.post(
            f"/accounts/send/{source_account_id.value}/{target_account_id.value}/{transfer_amount.amount}"
        )
        result_source_balance = self.client.get(f"/accounts/balance/{source_account_id.value}").json()
        result_target_balance = self.client.get(f"/accounts/balance/{target_account_id.value}").json()
        # await self.clean_db()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(result_source_balance, initial_source_balance - transfer_amount)

        self.assertEqual(result_target_balance, initial_target_balance + transfer_amount)

    async def init_test_db(self) -> None:
        container = Container()
        db = container.database()
        await db.create_database()
        with open("tests/resources/integration/send_money_integration_test.sql") as file:
            sql = file.read()

        sql_commands = sql.replace("\n", "").split(";")[:-1]
        sql_text_commands = [text(sql_command.strip()) for sql_command in sql_commands]

        async with db.session() as session:
            for sql_text_command in sql_text_commands:
                await session.execute(sql_text_command)
            await session.commit()

    async def clean_db(self) -> None:
        container = Container()
        db = container.database()
        await db.drop_database()
