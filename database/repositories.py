from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result

from .models import book, user, address as addr, order, order_item

class BookRepository():
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.db_session.enable_relationship_loading()


    async def create_book(self, name: str, author: str,   release_year: int):
        new_book = book.Book(name=name,author=author, release_year=release_year)
        self.db_session.add(new_book)
        await self.db_session.flush()


    async def get_all_books(self) -> list[book.Book]:
        q = await self.db_session.execute(select(book.Book).order_by(book.Book.id))
        return q.scalars().all()


    async def update_book(self, book_id: int, name: str | None, author: str | None, release_year: str | None):
        q = update(book.Book).where(book.Book.id == book_id)
        if name:
            q = q.values(name=name)
        if author:
            q = q.values(author=author)
        if release_year:
            q = q.values(release_year=release_year)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
    

    async def delete_book(self, book_id: int):
        q = delete(book.Book).where(book.Book.id == book_id)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)


class UserRepository():
    def __init__(self, db_session: Session):
        self.db_session = db_session
    

    async def create_user(self, username: str, password: str, full_name: str):
        new_user = user.User(
            username=username, 
            hashed_password=password,
            full_name=full_name)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    
    async def get_user_by_username(self, username: str):
        res: Result = await self.db_session.execute(select(user.User).where(user.User.username == username))
        return res.scalars().first()


class AddressRepository():
    def __init__(self, db_session: Session):
        self.db_session = db_session
    

    async def create_address(self, user_id: int, address: str):
        new_address = addr.Address(user_id=user_id, address=address)
        self.db_session.add(new_address)
        await self.db_session.flush()


class OrderRepository():
    def __init__(self, db_session: Session):
        self.db_session = db_session
    

    async def create_order(self, order: order.CreateOrderDto):
        new_order = order.Order(
            user_id=order.id,
            order_date=order.order_date,
            general_cost=order.general_cost,
            address=order.address,
            status=order.status)
        self.db_session.add(new_order)
        await self.db_session.flush()


class OrderItemRepository():
    def __init__(self, db_session: Session):
        self.db_session = db_session
    

    async def create_order_item(self, order_id: int, description: str, cost: float):
        new_order_item = order_item.OrderItem(
            order_id=order_id,
            description=description,
            cost=cost)
        self.db_session.add(new_order_item)
        await self.db_session.flush()