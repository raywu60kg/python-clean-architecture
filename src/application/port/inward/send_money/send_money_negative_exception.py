from src.application.domain.entity.money import Money


class SendMoneyNegativeException(Exception):
    def __init__(self, money: Money):
        super().__init__(f"Send money has to be positive but got negative money: {money.amount}!")
