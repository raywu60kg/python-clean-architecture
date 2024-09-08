from unittest import TestCase

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.adapter.outward.persistence.database import Base
from src.application.domain.entity.account import AccountId
from src.application.domain.entity.money import Money


class SendMoneySystemTest(TestCase):
    @pytest.fixture(autouse=True)
    def request_fixture(self, client: TestClient) -> None:
        self.client = client

    def test_send_money(self) -> None:
        self.init_test_db()

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

        self.clean_db()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(result_source_balance, initial_source_balance - transfer_amount.amount)

        self.assertEqual(result_target_balance, initial_target_balance + transfer_amount.amount)

    def init_test_db(self) -> None:
        engine = create_engine("postgresql+psycopg2://pca:pca@localhost:5432/pca", echo=True)

        Base.metadata.create_all(engine)
        with open("tests/resources/integration/send_money_integration_test.sql") as file:
            sql = file.read()

        sql_commands = sql.replace("\n", "").split(";")[:-1]
        sql_text_commands = [text(sql_command.strip()) for sql_command in sql_commands]
        session_factory = sessionmaker(bind=engine)

        with session_factory() as session:
            for sql_text_command in sql_text_commands:
                session.execute(sql_text_command)
            session.commit()

    def clean_db(self) -> None:
        engine = create_engine("postgresql+psycopg2://pca:pca@localhost:5432/pca", echo=True)
        Base.metadata.drop_all(engine)
