from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.adapter.outward.persistence.database import Base


class ActivitySqlalchemyBase(Base):
    __tablename__ = "activity"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    owner_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("account.id"), nullable=False)
    source_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("account.id"), nullable=False)
    target_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("account.id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer)
