from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """Base interface for all repositories"""
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Adds a new entity"""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Finds an entity by ID"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Updates an existing entity"""
        pass
    
    @abstractmethod
    def delete(self, entity: T) -> None:
        """Removes an entity"""
        pass


class IUserRepository(IRepository):
    """Specific interface for User repository"""
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[T]:
        """Finds a user by email"""
        pass
    
    @abstractmethod
    def get_by_document(self, document: str) -> Optional[T]:
        """Finds a user by document"""
        pass
    
    @abstractmethod
    def list_all(self) -> List[T]:
        """Lists all users"""
        pass


class IAccountRepository(IRepository):
    """Specific interface for Account repository"""
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[T]:
        """Finds an account by user ID"""
        pass


class ITransactionRepository(IRepository):
    """Specific interface for Transaction repository"""
    
    @abstractmethod
    def list_by_user(self, user_id: int) -> List[T]:
        """Lists transactions of a given user"""
        pass
    
    @abstractmethod
    def list_pending(self) -> List[T]:
        """Lists pending transactions"""
        pass
