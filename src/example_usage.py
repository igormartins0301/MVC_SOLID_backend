"""
Exemplo de uso da estrutura MVC com SOLID e Object Calisthenics
"""
from decimal import Decimal
from src.database import SessionLocal
from src.container import Container
from src.controllers.user_controller import UserController


def main():
    """Exemplo de uso da estrutura"""
    
    # Cria uma sessão do banco
    session = SessionLocal()
    
    try:
        # Configura o container de dependências
        container = Container(session)
        
        # Obtém os services
        user_service = container.get_user_service()
        account_service = container.get_account_service()
        transaction_service = container.get_transaction_service()
        
        # Obtém o controller
        user_controller = UserController(user_service)
        
        # Exemplo: Criar um usuário
        user_data = {
            "name": "João Silva",
            "email": "joao@example.com",
            "document": "12345678901",
            "password": "123456",
            "user_type": "user"
        }
        
        result = user_controller.create_user(user_data)
        print("Criar usuário:", result)
        
        if result["success"]:
            user_id = result["data"]["id"]
            
            # Exemplo: Criar uma conta para o usuário
            account = account_service.create_account(user_id, Decimal("100.00"))
            print(f"Conta criada com saldo: R$ {account.balance}")
            
            # Exemplo: Criar outro usuário para transferência
            user2_data = {
                "name": "Maria Santos",
                "email": "maria@example.com",
                "document": "98765432100",
                "password": "123456",
                "user_type": "user"
            }
            
            result2 = user_controller.create_user(user2_data)
            if result2["success"]:
                user2_id = result2["data"]["id"]
                account2 = account_service.create_account(user2_id, Decimal("50.00"))
                
                # Exemplo: Realizar transferência
                try:
                    transaction = transaction_service.transfer(
                        sender_id=user_id,
                        receiver_id=user2_id,
                        amount=Decimal("25.00")
                    )
                    print(f"Transferência realizada: R$ {transaction.amount}")
                    
                    # Verificar saldos após transferência
                    sender_account = account_service.get_by_user_id(user_id)
                    receiver_account = account_service.get_by_user_id(user2_id)
                    
                    print(f"Saldo do remetente: R$ {sender_account.balance}")
                    print(f"Saldo do destinatário: R$ {receiver_account.balance}")
                    
                except ValueError as e:
                    print(f"Erro na transferência: {e}")
        
        # Exemplo: Listar usuários
        users_result = user_controller.list_users()
        print("Lista de usuários:", users_result)
        
    finally:
        session.close()


if __name__ == "__main__":
    main() 