from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.accounts import Account


class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, account: Account) -> Account:
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    def get_by_id(self, account_id: int) -> Optional[Account]:
        return self.session.query(Account).filter(Account.id == account_id).first()

    def get_by_user_id(self, user_id: int) -> Optional[Account]:
        return self.session.query(Account).filter(Account.user_id == user_id).first()

    def update(self, account: Account) -> Account:
        self.session.commit()
        self.session.refresh(account)
        return account

    def delete(self, account: Account) -> None:
        self.session.delete(account)
        self.session.commit()
