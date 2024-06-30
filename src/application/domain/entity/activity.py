from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .account import AccountId
from .money import Money


class ActivityId(BaseModel):
    value: int


class Activity(BaseModel):
    activity_id: Optional[ActivityId] = None
    owner_account_id: Optional[AccountId]
    source_account_id: Optional[AccountId]
    target_account_id: Optional[AccountId]
    timestamp: datetime
    money: Money
