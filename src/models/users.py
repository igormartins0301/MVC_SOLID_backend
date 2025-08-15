from sqlalchemy import Column, Integer, String, Enum as SAEnum, UniqueConstraint, Boolean, text
from sqlalchemy.orm import relationship
from dataclasses import dataclass
from enum import Enum

from src.database import Base
class UserType(str, Enum):
    USER = "user"
    SELLER = "seller"
    
class Email:
    def __init__(self, address: str):
        if  "@" not in address or "." not in address.split("@")[-1]:
            raise ValueError("Invalid email address")
        self.address = address.strip().lower()
        
    def __str__(self) -> str:
        return self.address

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email= Column(String, nullable=False, unique=True, index=True)
    document = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    user_type = Column(SAEnum(UserType) , nullable=False)
    active = Column(Boolean, nullable=False, server_default=text("True"))
    
    __table_args__ = (
        UniqueConstraint("email", name = "uq_users_email"),
        UniqueConstraint("document", name = "uq_users_document"),
    )
    
    def __init__(self, name: str, email: Email, document: str, password: str, user_type: UserType):
        if not name.strip():
            raise ValueError("Name cannot be empty")
        if not document.strip():
            raise ValueError("Document cannot be empty")
        if len(password) < 6:
            raise ValueError("Password must have at least 6 characters")
        
        self.name = name.strip()
        self.email = str(email)
        self.document = document.strip()
        self.password = password
        self.user_type = user_type
        
        super().__init__(**kwargs)

    def deactivate(self):
        self.active = False
    
    def activate(self):
        self.active = True
        
    
    