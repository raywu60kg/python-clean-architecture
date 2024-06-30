class AccountNotFoundException(Exception):
    def __init__(self, account_id: int):
        super().__init__(f"Account not found: {account_id}!")
