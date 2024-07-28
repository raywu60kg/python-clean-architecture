from src.application.domain.entity.account import AccountId


class SendMoneyAccountNotFoundException(Exception):
    def __init__(self, from_account_id: AccountId | None, to_account_id: AccountId | None):
        super().__init__(f"Both account id need to existed but got from: {from_account_id}, to:{to_account_id}!")
