from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AccountSqlalchemyBase(DeclarativeBase):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
