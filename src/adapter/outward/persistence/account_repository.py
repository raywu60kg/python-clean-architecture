from .account_sqlalchemy_base import AccountSqlalchemyBase


class AccountRepository:
    def findById(self, account_id: int) -> AccountSqlalchemyBase:
        pass
