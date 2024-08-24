from datetime import datetime
from unittest import TestCase

from src.application.domain.entity.account import AccountId
from src.application.domain.entity.activity_window import ActivityWindow
from src.application.domain.entity.money import Money
from tests.common.activity_test_builder import ActivityTestBuilder


class TestActivityWindow(TestCase):
    start_date = datetime(2019, 8, 3, 0, 0)
    in_between_date = datetime(2019, 8, 4, 0, 0)
    end_date = datetime(2019, 8, 5, 0, 0)

    def test_calculates_start_timestamp(self) -> None:
        window = ActivityWindow(
            [
                ActivityTestBuilder().with_timestamp(self.start_date).build(),
                ActivityTestBuilder().with_timestamp(self.in_between_date).build(),
                ActivityTestBuilder().with_timestamp(self.end_date).build(),
            ]
        )
        self.assertEqual(window.get_start_time(), self.start_date)

    def test_calculates_end_timestamp(self) -> None:
        window = ActivityWindow(
            [
                ActivityTestBuilder().with_timestamp(self.start_date).build(),
                ActivityTestBuilder().with_timestamp(self.in_between_date).build(),
                ActivityTestBuilder().with_timestamp(self.end_date).build(),
            ]
        )
        self.assertEqual(window.get_end_time(), self.end_date)

    def test_calculates_balance(self) -> None:
        account1 = AccountId(1)
        account2 = AccountId(2)

        window = ActivityWindow(
            [
                ActivityTestBuilder()
                .with_money(Money(999))
                .with_source_account(account1)
                .with_target_account(account2)
                .with_timestamp(self.start_date)
                .build(),
                ActivityTestBuilder()
                .with_money(Money(1))
                .with_source_account(account1)
                .with_target_account(account2)
                .with_timestamp(self.in_between_date)
                .build(),
                ActivityTestBuilder()
                .with_money(Money(500))
                .with_source_account(account2)
                .with_target_account(account1)
                .with_timestamp(self.end_date)
                .build(),
            ]
        )
        self.assertEqual(window.calculate_balance(account1), Money(-500))  # type: ignore
        self.assertEqual(window.calculate_balance(account2), Money(500))  # type: ignore
