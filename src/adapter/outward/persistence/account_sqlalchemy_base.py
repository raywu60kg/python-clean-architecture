from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.adapter.outward.persistence.database import Base


class AccountSqlalchemyBase(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
