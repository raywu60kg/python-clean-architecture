from unittest import TestCase

from src.application.domain.entity.account import Account, AccountId
from src.application.domain.entity.activity import Activity
from src.application.domain.entity.activity_window import ActivityWindow
from src.application.domain.entity.money import Money


class TestAccount(TestCase):
    def test_calculates_balance(self):
        account_id = AccountId(1)
        account = Account(
            account_id=account_id,
            baseline_balance=Money(555),
            activity_window=ActivityWindow(
                [
                    Activity.with_target_account(account_id).with_money(Money.of(999)),
                    Activity.with_target_account(account_id).with_money(Money.of(1)),
                ]
            ),
        )

        balance = account.calculate_balance()

        self.assertEqual(balance.amount, 1555)

    def test_withdrawal_succeeds(self):
        account_id = AccountId(1)
        account = Account(
            account_id=account_id,
            baseline_balance=Money.of(555),
            activity_window=ActivityWindow(
                [
                    Activity.with_target_account(account_id).with_money(Money.of(999)),
                    Activity.with_target_account(account_id).with_money(Money.of(1)),
                ]
            ),
        )

        random_target_account = AccountId(99)
        success = account.withdraw(Money.of(555), random_target_account)

        self.assertTrue(success)
        self.assertEqual(len(account.activity_window.activities), 3)
        self.assertEqual(account.calculate_balance().amount, 1000)

    def test_withdrawal_failure(self):
        account_id = AccountId(1)
        account = Account(
            account_id=account_id,
            baseline_balance=Money.of(555),
            activity_window=ActivityWindow(
                [
                    Activity.with_target_account(account_id).with_money(Money.of(999)),
                    Activity.with_target_account(account_id).with_money(Money.of(1)),
                ]
            ),
        )

        success = account.withdraw(Money.of(1556), AccountId(99))

        self.assertFalse(success)
        self.assertEqual(len(account.activity_window.activities), 2)
        self.assertEqual(account.calculate_balance().amount, 1555)

    def test_deposit_success(self):
        account_id = AccountId(1)
        account = Account(
            account_id=account_id,
            baseline_balance=Money.of(555),
            activity_window=ActivityWindow(
                [
                    Activity.with_target_account(account_id).with_money(Money.of(999)),
                    Activity.with_target_account(account_id).with_money(Money.of(1)),
                ]
            ),
        )

        success = account.deposit(Money.of(445), AccountId(99))

        self.assertTrue(success)
        self.assertEqual(len(account.activity_window.activities), 3)
        self.assertEqual(account.calculate_balance().amount, 2000)
