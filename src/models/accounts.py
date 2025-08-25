from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from src.database import Base
from decimal import Decimal
from enum import Enum


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    balance = Column(Numeric(10, 2), nullable=False)

    user = relationship("User", foreign_keys=[user_id])

    def __init__(self, user_id: int, balance: Decimal = Decimal("0.00")):
        if balance < Decimal("0.00"):
            raise ValueError("Balance cannot be negative")
        self.user_id = user_id
        self.balance = balance

    def deposit(self, amount: Decimal):
        if amount <= Decimal("0.00"):
            raise ValueError("Amount must be positive")
        self.balance += amount

    def withdraw(self, amount: Decimal):
        if amount <= Decimal("0.00"):
            raise ValueError("Amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount

    def has_sufficient_balance(self, amount: Decimal) -> bool:
        return self.balance >= amount
