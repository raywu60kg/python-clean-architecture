from unittest import TestCase

import pytest

from src.application.domain.entity.account import AccountId
from src.application.domain.entity.money import Money
from src.application.port.inward.send_money.send_money_command import SendMoneyCommand
from src.application.port.inward.send_money.send_money_negative_exception import SendMoneyNegativeException


class TestSendMoneyCommand(TestCase):
    def test_validation_ok(self) -> None:
        SendMoneyCommand(source_account_id=AccountId(42), target_account_id=AccountId(43), money=Money(10))
        assert True

    def test_money_validation_fails(self) -> None:
        with pytest.raises(SendMoneyNegativeException):
            SendMoneyCommand(
                source_account_id=AccountId(42),
                target_account_id=AccountId(43),
                money=Money(-10),
            )
