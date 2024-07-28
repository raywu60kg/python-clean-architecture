from src.application.domain.entity.money import Money


class ThresholdExceededException(Exception):
    def __init__(self, threshold: Money, actual: Money):
        super().__init__(
            f"Maximum threshold for transferring money exceeded: tried to transfer {actual.amount} but threshold is {threshold.amount}!"
        )
