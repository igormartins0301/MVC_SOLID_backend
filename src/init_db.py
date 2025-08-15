from src.database import Base, engine
from src.models import Account, Transaction, User

Base.metadata.create_all(bind=engine)