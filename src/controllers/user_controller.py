"""
Controller para gerenciar operações de usuários
"""
from typing import Dict, Any
from src.services.interfaces import IUserService
from src.models.users import User


class UserController:
    """Controller para operações de usuários"""
    
    def __init__(self, user_service: IUserService):
        self.user_service = user_service
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo usuário"""
        try:
            user = self.user_service.create_user(
                name=user_data["name"],
                email=user_data["email"],
                document=user_data["document"],
                password=user_data["password"],
                user_type=user_data["user_type"]
            )
            
            return {
                "success": True,
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "user_type": user.user_type.value,
                    "active": user.active
                }
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Internal server error"
            }
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Busca um usuário por ID"""
        try:
            user = self.user_service.get_user(user_id)
            if not user:
                return {
                    "success": False,
                    "error": "User not found"
                }
            
            return {
                "success": True,
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "user_type": user.user_type.value,
                    "active": user.active
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Internal server error"
            }
    
    def list_users(self) -> Dict[str, Any]:
        """Lista todos os usuários"""
        try:
            users = self.user_service.list_users()
            return {
                "success": True,
                "data": [
                    {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "user_type": user.user_type.value,
                        "active": user.active
                    }
                    for user in users
                ]
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Internal server error"
            } 