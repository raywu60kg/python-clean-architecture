from datetime import datetime

from src.application.domain.entity.money import Money
from src.application.port.inward.get_account_balance.get_account_balance_query import GetAccountBalanceQuery
from src.application.port.inward.get_account_balance.get_account_balance_use_case import GetAccountBalanceUseCase
from src.application.port.outward.load_account_port import LoadAccountPort


class GetAccountBalanceService(GetAccountBalanceUseCase):
    def __init__(self, load_account_port: LoadAccountPort) -> None:
        self.__load_account_port = load_account_port

    def get_account_balance(self, query: GetAccountBalanceQuery) -> Money:
        return self.__load_account_port.load_account(query.account_id, datetime.now()).calculate_balance()
