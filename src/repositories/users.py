from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.users import User, UserType, Email


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def get_by_document(self, document: str) -> Optional[User]:
        return self.session.query(User).filter(User.document == document).first()

    def list_all(self) -> List[User]:
        return self.session.query(User).all()

    def update(self, user: User) -> User:
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
