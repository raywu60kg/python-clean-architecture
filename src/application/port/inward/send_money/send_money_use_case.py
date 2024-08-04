from abc import ABC, abstractmethod

from src.application.port.inward.send_money.send_money_command import SendMoneyCommand


class SendMoneyUseCase(ABC):
    @abstractmethod
    async def send_money(self, command: SendMoneyCommand) -> bool:
        pass
