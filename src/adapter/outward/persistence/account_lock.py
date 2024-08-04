from src.application.domain.entity.account import AccountId
from src.application.port.outward.account_lock import AccountLock


class AccountPersistenceLocker(AccountLock):
    def lock_account(self, account_id: AccountId) -> None:
        pass

    def release_account(self, account_id: AccountId) -> None:
        pass
