from decimal import Decimal
from typing import Optional

from src.models.accounts import Account
from src.repositories.interfaces import IAccountRepository
from src.services.interfaces import IAccountService

class AccountService(IAccountService):
    def __init__(self, repository: IAccountRepository[Account]):
        self.repository = repository
    
    def create_account(self, user_id: int, initial_balance: Decimal = Decimal("0.00")) -> Account:
        if self.repository.get_by_user_id(user_id) is not None:
            raise ValueError("User already has an account")
        
        account = Account(user_id=user_id, balance=initial_balance)
        return self.repository.add(account)
    
    def get_account(self, account_id: int) -> Optional[Account]:
        return self.repository.get_by_id(account_id)
    
    def get_by_user_id(self, user_id: int) -> Optional[Account]:
        return self.repository.get_by_user_id(user_id)
    
    def deposit(self, account_id: int, amount: Decimal) -> Account:
        account = self._get_account_or_raise(account_id)
        account.deposit(amount)
        return self.repository.update(account)

    def withdraw(self, account_id: int, amount: Decimal) -> Account:
        account = self._get_account_or_raise(account_id)
        account.withdraw(amount)
        return self.repository.update(account)
        
    def _get_account_or_raise(self, account_id: int) -> Account:
        account = self.repository.get_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        return account