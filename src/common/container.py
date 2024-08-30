from dependency_injector import containers, providers

from src.adapter.outward.persistence.account_lock import AccountPersistenceLocker
from src.adapter.outward.persistence.account_mapper import AccountMapper
from src.adapter.outward.persistence.account_persistence_adapter import AccountPersistenceAdapter
from src.adapter.outward.persistence.account_repository import AccountRepository
from src.adapter.outward.persistence.activity_repository import ActivityRepository
from src.adapter.outward.persistence.database import Database
from src.application.domain.service.get_account_balance.get_account_balance_service import GetAccountBalanceService
from src.application.domain.service.send_money.money_transfer_properties import MoneyTransferProperties
from src.application.domain.service.send_money.send_money_service import SendMoneyService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.db_uri.from_env("DB_URI", "postgresql+asyncpg://pca:pca@localhost:5432/pca")
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.adapter.inward.web.router",
        ]
    )
    database = providers.Singleton(Database, db_uri=config.db_uri)

    account_repository = providers.Factory(
        AccountRepository,
        session_factory=database.provided.session,
    )
    activity_repository = providers.Factory(
        ActivityRepository,
        session_factory=database.provided.session,
    )
    account_mapper = providers.Factory(AccountMapper)

    account_persistence_adapter = providers.Factory(
        AccountPersistenceAdapter,
        account_mapper=account_mapper,
        account_repository=account_repository,
        activity_repository=activity_repository,
    )

    get_account_balance_service = providers.Factory(
        GetAccountBalanceService, load_account_port=account_persistence_adapter
    )
    account_persistence_locker = providers.Factory(AccountPersistenceLocker)
    money_transfer_properties = providers.Factory(MoneyTransferProperties)

    send_money_service = providers.Factory(
        SendMoneyService,
        load_account_port=account_persistence_adapter,
        account_lock=account_persistence_locker,
        update_account_state_port=account_persistence_adapter,
        money_transfer_properties=money_transfer_properties,
    )
