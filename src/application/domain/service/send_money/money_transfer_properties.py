from src.application.domain.entity.money import Money


class MoneyTransferProperties:
    __maximum_transfer_threshold: Money = Money(1_000_000)

    @property
    def maximum_transfer_threshold(self) -> Money:
        return self.__maximum_transfer_threshold
