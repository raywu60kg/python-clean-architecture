from ....port.inward.send_money.send_money_use_case import SendMoneyUseCase
from ....port.outward.load_account_port import LoadAccountPort


class SendMoneyService(SendMoneyUseCase):
    def __init__(self, load_account_port: LoadAccountPort) -> None:
        self.__load_account_port = load_account_port
        pass
