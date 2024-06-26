from abc import ABC, abstractmethod

from .send_money_command import SendMoneyCommand


class SendMoneyUseCase(ABC):
    @abstractmethod
    def send_money(self, command: SendMoneyCommand) -> bool:
        pass
