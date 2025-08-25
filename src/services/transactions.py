from decimal import Decimal
from sqlalchemy.orm import Session
from src.models.transactions import Transaction
from src.models.users import UserType
from src.repositories.interfaces import ITransactionRepository
from src.services.interfaces import IAccountService, ITransactionService, IAuthorizerService


class TransactionService(ITransactionService):
    def __init__(
        self, 
        session: Session, 
        transaction_repository: ITransactionRepository[Transaction], 
        account_service: IAccountService,
        authorizer_service: IAuthorizerService
    ):
        self.session = session
        self.transaction_repository = transaction_repository
        self.account_service = account_service
        self.authorizer_service = authorizer_service
    
    def transfer(self, sender_id: int, receiver_id: int, amount: Decimal) -> Transaction:
        self._validate_transfer_request(sender_id, receiver_id, amount)
        
        with self.session.begin():
            self._validate_authorization()

            sender_account = self._get_sender_account(sender_id)
            receiver_account = self._get_receiver_account(receiver_id)
            
            self._validate_sender_can_transfer(sender_account, amount)
            
            self._execute_transfer(sender_account, receiver_account, amount)
            
            transaction = self._create_transaction(sender_id, receiver_id, amount)
            self._notify_transfer(sender_id, receiver_id, amount)
            return transaction
        
    def _validate_authorization(self) -> None:
        if not self.authorizer_service.is_authorized():
            raise ValueError("Transfer not authorized by external service")

    def _validate_transfer_request(self, sender_id: int, receiver_id: int, amount: Decimal) -> None:
        if amount <= Decimal("0"):
            raise ValueError("Amount must be positive")
        
        if sender_id == receiver_id:
            raise ValueError("Sender and receiver cannot be the same")
    
    def _get_sender_account(self, sender_id: int):
        sender_account = self.account_service.get_by_user_id(sender_id)
        if not sender_account:
            raise ValueError("Sender account not found")
        return sender_account
    
    def _get_receiver_account(self, receiver_id: int):
        receiver_account = self.account_service.get_by_user_id(receiver_id)
        if not receiver_account:
            raise ValueError("Receiver account not found")
        return receiver_account
    
    def _validate_sender_can_transfer(self, sender_account, amount: Decimal) -> None:
        if sender_account.user.user_type == UserType.SELLER:
            raise ValueError("Sellers cannot send money")
        
        if not sender_account.has_sufficient_balance(amount):
            raise ValueError("Insufficient balance")
    
    def _execute_transfer(self, sender_account, receiver_account, amount: Decimal) -> None:
        sender_account.withdraw(amount)
        receiver_account.deposit(amount)
        
        self.account_service.repository.update(sender_account)
        self.account_service.repository.update(receiver_account)
    
    def _create_transaction(self, sender_id: int, receiver_id: int, amount: Decimal) -> Transaction:
        transaction = Transaction(
            sender_id=sender_id, 
            receiver_id=receiver_id, 
            amount=amount
        )
        return self.transaction_repository.add(transaction)

    def _notify_transfer(self, sender_id: int, receiver_id: int, amount: Decimal) -> None:
        self.notify_service.notify(f"Transfer of {amount} from {sender_id} to {receiver_id} completed")
            