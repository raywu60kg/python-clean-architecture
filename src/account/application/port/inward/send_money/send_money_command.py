class SendMoneyCommand:
    def __init__(self, source_account_id: str, target_account_id: str, amount: float) -> None:
        self.__source_account_id = source_account_id
        self.__target_account_id = target_account_id
        self.amount = amount

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        if value < 0:
            raise ValueError(f"Amount has to be positive but got {value}")
        self.__amount = value
