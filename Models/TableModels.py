from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Float, DateTime, func, Integer
from dataclasses import dataclass


@dataclass
class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


@dataclass
class Attributes(Base):
    __tablename__ = 'Attributes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    age: Mapped[str] = mapped_column(Text)
    city: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    description: Mapped[str] = mapped_column(String(150))
    id_telegram_user: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    messages: Mapped[int] = mapped_column(Integer, nullable=False)
    strikes: Mapped[int] = mapped_column(Integer, nullable=False)
