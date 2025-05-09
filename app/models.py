from app.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))

def __init__(self, username, email, hashed_password):
    self.username = username
    self.email = email
    self.hashed_password = hashed_password




