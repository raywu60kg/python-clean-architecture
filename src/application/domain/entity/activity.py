from datetime import datetime

from src.application.domain.entity.money import Money


class ActivityId:
    def __init__(self, value: int) -> None:
        self.__value = value

    @property
    def value(self) -> int:
        return self.__value


class Activity:
    def __init__(
        self,
        owner_account_id: "AccountId",  # type: ignore  # noqa: F821
        source_account_id: "AccountId",  # type: ignore  # noqa: F821
        target_account_id: "AccountId",  # type: ignore  # noqa: F821
        timestamp: datetime,
        money: Money,
        activity_id: ActivityId | None = None,
    ) -> None:
        self.__activity_id = activity_id
        self.__owner_account_id = owner_account_id  # type: ignore
        self.__source_account_id = source_account_id  # type: ignore
        self.__target_account_id = target_account_id  # type: ignore
        self.__timestamp = timestamp
        self.__money = money

    @property
    def activity_id(self) -> ActivityId | None:
        return self.__activity_id

    @property
    def owner_account_id(self) -> "AccountId":  # type: ignore # noqa: F821
        return self.__owner_account_id  # type: ignore

    @property
    def source_account_id(self) -> "AccountId":  # type: ignore # noqa: F821
        return self.__source_account_id  # type: ignore

    @property
    def target_account_id(self) -> "AccountId":  # type: ignore # noqa: F821
        return self.__target_account_id  # type: ignore

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @property
    def money(self) -> Money:
        return self.__money
