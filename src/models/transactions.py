from sqlalchemy import Column, Integer, Numeric, DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database import Base
from decimal import Decimal
from enum import Enum

class Status(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount= Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status= Column(SAEnum(Status), nullable=False, default=Status.PENDING)
    
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    
    def __init__(self, sender_id: int, receiver_id: int, amount: Decimal):
        if amount <= Decimal("0"):
            raise ValueError("Amount must be positive")
        
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.status = Status.PENDING
    
    def approve(self):
        if self.status != Status.PENDING:
            raise ValueError("Transaction is not pending")
        self.status = Status.APPROVED
    
    def reject(self):
        if self.status != Status.PENDING:
            raise ValueError("Transaction is not pending")
        self.status = Status.REJECTED
    
    def is_complete(self) -> bool:
        return self.status in {Status.APPROVED, Status.REJECTED}