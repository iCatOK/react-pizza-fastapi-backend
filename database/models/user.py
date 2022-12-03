from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..config import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)

    addresses = relationship("Address", back_populates="user", lazy="joined")
    orders = relationship("Order", back_populates="user", lazy="joined")

    def __str__(self):
        return f'User: id={self.id}, username={self.username}, hashed_password={self.hashed_password}'