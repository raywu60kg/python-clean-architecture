from unittest import TestCase

from src.application.domain.entity.account import AccountId
from src.application.domain.entity.activity_window import ActivityWindow
from src.application.domain.entity.money import Money
from tests.common.account_test_builder import AccountTestBuilder
from tests.common.activity_test_builder import ActivityTestBuilder


class TestAccount(TestCase):
    test_account_id = AccountId(1)

    def test_calculates_balance(self) -> None:
        account = (
            AccountTestBuilder()
            .with_account_id(account_id=self.test_account_id)
            .with_baseline_balance(baseline_balance=Money(555))
            .with_activity_window(
                activity_window=ActivityWindow(
                    activities=[
                        ActivityTestBuilder().with_target_account(self.test_account_id).with_money(Money(999)).build(),
                        ActivityTestBuilder().with_target_account(self.test_account_id).with_money(Money(1)).build(),
                    ]
                )
            )
        ).build()

        balance = account.calculate_balance()

        self.assertEqual(balance.amount, 1555)

    def test_withdrawal_succeeds(self) -> None:
        self.test_account_id = AccountId(1)
        account = (
            AccountTestBuilder()
            .with_account_id(account_id=self.test_account_id)
            .with_baseline_balance(baseline_balance=Money(555))
            .with_activity_window(
                activity_window=ActivityWindow(
                    activities=[
                        ActivityTestBuilder().with_target_account(self.test_account_id).with_money(Money(999)).build(),
                        ActivityTestBuilder().with_target_account(self.test_account_id).with_money(Money(1)).build(),
                    ]
                )
            )
        ).build()

        random_target_account = AccountId(99)
        success = account.withdraw(Money(555), random_target_account)

        self.assertTrue(success)
        self.assertEqual(len(account.activity_window.activities), 3)
        self.assertEqual(account.calculate_balance().amount, 1000)

    def test_withdrawal_failure(self) -> None:
        self.test_account_id = AccountId(1)
        account = (
            AccountTestBuilder()
            .with_account_id(account_id=self.test_account_id)
            .with_baseline_balance(baseline_balance=Money(555))
            .with_activity_window(
                activity_window=ActivityWindow(
                    activities=[
                        ActivityTestBuilder().with_target_account(self.test_account_id).with_money(Money(999)).build(),
                        ActivityTestBuilder().with_target_account(self.test_account_id).with_money(Money(1)).build(),
                    ]
                )
            )
        ).build()

        success = account.withdraw(Money(1556), AccountId(99))

        self.assertFalse(success)
        self.assertEqual(len(account.activity_window.activities), 2)
        self.assertEqual(account.calculate_balance().amount, 1555)

    def test_deposit_success(self) -> None:
        self.test_account_id = AccountId(1)
        account = (
            AccountTestBuilder()
            .with_account_id(account_id=self.test_account_id)
            .with_baseline_balance(baseline_balance=Money(555))
            .with_activity_window(
                activity_window=ActivityWindow(
                    activities=[
                        ActivityTestBuilder().with_target_account(self.test_account_id).with_money(Money(999)).build(),
                        ActivityTestBuilder().with_target_account(self.test_account_id).with_money(Money(1)).build(),
                    ]
                )
            )
        ).build()

        success = account.deposit(Money(445), AccountId(99))

        self.assertTrue(success)
        self.assertEqual(len(account.activity_window.activities), 3)
        self.assertEqual(account.calculate_balance().amount, 2000)
