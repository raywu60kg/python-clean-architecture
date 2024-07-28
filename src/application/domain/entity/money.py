from __future__ import annotations


class Money:
    def __init__(self, value: int) -> None:
        self.__amount: int = value

    @property
    def amount(self) -> int:
        return self.__amount

    def is_positive_or_zero(self) -> bool:
        return self.__amount >= 0

    def is_negative(self) -> bool:
        return self.__amount < 0

    def is_positive(self) -> bool:
        return self.__amount > 0

    def is_greater_than_or_equal_to(self, money: Money) -> bool:
        return self.__amount >= money.amount

    def is_greater_than(self, money: Money) -> bool:
        return self.__amount > money.amount

    def __add__(self, other: Money) -> Money:
        return Money(self.__amount + other.amount)

    def __sub__(self, other: Money) -> Money:
        return Money(self.__amount - other.amount)

    def __neg__(self) -> Money:
        return Money(-self.__amount)

    @classmethod
    def create(cls, value: int) -> Money:
        return cls(value=value)
