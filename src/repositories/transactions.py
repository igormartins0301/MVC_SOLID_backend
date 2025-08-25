from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.transactions import Transaction, Status


class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        return (
            self.session.query(Transaction)
            .filter(Transaction.id == transaction_id)
            .first()
        )

    def list_by_user(self, user_id: int) -> List[Transaction]:
        return (
            self.session.query(Transaction)
            .filter(
                (Transaction.sender_id == user_id)
                | (Transaction.receiver_id == user_id)
            )
            .order_by(Transaction.created_at.desc())
            .all()
        )

    def list_pending(self) -> List[Transaction]:
        return (
            self.session.query(Transaction)
            .filter(Transaction.status == Status.PENDING)
            .order_by(Transaction.created_at.asc())
            .all()
        )

    def update(self, transaction: Transaction) -> Transaction:
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def delete(self, transaction: Transaction) -> None:
        self.session.delete(transaction)
        self.session.commit()
