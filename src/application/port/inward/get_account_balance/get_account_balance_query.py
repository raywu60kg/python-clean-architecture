from src.application.domain.entity.account import AccountId


class GetAccountBalanceQuery:
    def __init__(self, account_id: AccountId) -> None:
        self.__account_id = account_id

    @property
    def account_id(self) -> AccountId:
        return self.__account_id
