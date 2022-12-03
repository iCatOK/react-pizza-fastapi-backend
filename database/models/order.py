from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import date

from ..config import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_date = Column(Date)
    general_cost = Column(Float)
    status = Column(Integer)
    address = Column(String)

    user = relationship("User", back_populates="orders", lazy="joined")
    order_items = relationship("OrderItem", back_populates="order", lazy="joined")


class CreateOrderDto(BaseModel):
    order_date: date
    user_id: int
    general_cost: float
    status: int | None = 1
    address: str