"""
Container de dependências para inversão de controle
"""
from sqlalchemy.orm import Session
from src.repositories.users import UserRepository
from src.repositories.accounts import AccountRepository
from src.repositories.transactions import TransactionRepository
from src.services.users import UserService
from src.services.accounts import AccountService
from src.services.transactions import TransactionService
from src.services.auth import AuthorizerService
from src.services.notify import NotifyService


class Container:
    """Container simples para gerenciar dependências"""
    
    def __init__(self, session: Session):
        self.session = session
        self._setup_repositories()
        self._setup_services()
    
    def _setup_repositories(self):
        """Configura os repositories"""
        self.user_repository = UserRepository(self.session)
        self.account_repository = AccountRepository(self.session)
        self.transaction_repository = TransactionRepository(self.session)
    
    def _setup_services(self):
        """Configura os services com suas dependências"""
        self.user_service = UserService(self.user_repository)
        self.account_service = AccountService(self.account_repository)
        self.authorizer_service = AuthorizerService()
        self.notify_service = NotifyService()
        self.transaction_service = TransactionService(
            self.session,
            self.transaction_repository,
            self.account_service,
            self.authorizer_service,
            self.notify_service
        )
    
    def get_user_service(self) -> UserService:
        return self.user_service
    
    def get_account_service(self) -> AccountService:
        return self.account_service
    
    def get_transaction_service(self) -> TransactionService:
        return self.transaction_service 