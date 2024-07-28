class AccountNotPersistedException(Exception):
    def __init__(self) -> None:
        super().__init__("Account do not have id yet but doing operations")
