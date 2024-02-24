class GetAccountBalanceQuery:
    def __init__(self, account_id: str):
        self.__account_id = account_id

    @property
    def account_id(self) -> str:
        return self.__account_id
