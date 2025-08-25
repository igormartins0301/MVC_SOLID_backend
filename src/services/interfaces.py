from abc import ABC, abstractmethod
from typing import Optional, List
from decimal import Decimal
from src.models.users import User
from src.models.accounts import Account
from src.models.transactions import Transaction


class IUserService(ABC):
    """Interface for User service"""
    
    @abstractmethod
    def create_user(
        self, name: str, email: str, document: str, password: str, user_type: str
    ) -> User:
        """Creates a new user"""
        pass
    
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        """Finds a user by ID"""
        pass
    
    @abstractmethod
    def list_users(self) -> List[User]:
        """Lists all users"""
        pass
    
    @abstractmethod
    def deactivate_user(self, user_id: int) -> User:
        """Deactivates a user"""
        pass
    
    @abstractmethod
    def activate_user(self, user_id: int) -> User:
        """Activates a user"""
        pass
    
    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        """Deletes a user"""
        pass


class IAccountService(ABC):
    """Interface for Account service"""
    
    @abstractmethod
    def create_account(self, user_id: int, initial_balance: Decimal = Decimal("0.00")) -> Account:
        """Creates a new account"""
        pass
    
    @abstractmethod
    def get_account(self, account_id: int) -> Optional[Account]:
        """Finds an account by ID"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Account]:
        """Finds an account by user ID"""
        pass
    
    @abstractmethod
    def deposit(self, account_id: int, amount: Decimal) -> Account:
        """Performs a deposit"""
        pass
    
    @abstractmethod
    def withdraw(self, account_id: int, amount: Decimal) -> Account:
        """Performs a withdrawal"""
        pass


class ITransactionService(ABC):
    """Interface for Transaction service"""
    
    @abstractmethod
    def transfer(self, sender_id: int, receiver_id: int, amount: Decimal) -> Transaction:
        """Performs a transfer between accounts"""
        pass 


class IAuthorizerService(ABC):
    """Interface for external Authorizer service"""

    @abstractmethod
    def is_authorized(self) -> bool:
        """Checks the external service to authorize the transaction"""
        pass


class INotifyService(ABC):
    """Interface for Notification service"""

    @abstractmethod
    def notify(self, message: str) -> None:
        """Sends a notification"""
        pass
