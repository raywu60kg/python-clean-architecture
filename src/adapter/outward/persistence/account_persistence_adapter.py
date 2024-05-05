from ....application.port.outward.load_account_port import LoadAccountPort
from ....application.port.outward.update_account_state_port import UpdateAccountStatePort


class AccountPersistenceAdapter(LoadAccountPort, UpdateAccountStatePort):
    pass
