from src.application.domain.entity.money import Money


class MoneyTransferProperties:
    def __init__(self, maximum_transfer_threshold: Money = Money(1_000_000)) -> None:
        self.__maximum_transfer_threshold = maximum_transfer_threshold

    @property
    def maximum_transfer_threshold(self) -> Money:
        return self.__maximum_transfer_threshold
