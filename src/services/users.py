from typing import Optional, List
from src.models.users import User, UserType, Email
from src.repositories.users import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(
        self, name: str, email: str, document: str, password: str, user_type: str
    ) -> User:
        if self.user_repository.get_by_email(email):
            raise ValueError("Email already exists")
        if self.user_repository.get_by_document(document):
            raise ValueError("Document already exists")

        user = User(
            name=name,
            email=email,
            document=document,
            password=password,
            user_type=UserType(user_type),
        )

        return self.user_repository.add(user)

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)

    def list_users(self) -> List[User]:
        return self.user_repository.list_all()

    def deactivate_user(self, user_id: int) -> User:
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        user.deactivate()
        return self.user_repository.update(user)

    def activate_user(self, user_id: int) -> User:
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        user.activate()
        return self.user_repository.update(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        return self.user_repository.delete(user)
