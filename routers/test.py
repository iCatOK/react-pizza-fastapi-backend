from fastapi import APIRouter
from database.config import async_session
from database.repositories import AddressRepository, BookRepository, UserRepository
from database.models.book import Book

router = APIRouter()

@router.post("/books")
async def create_book(name: str, author: str, release_year: int):
    async with async_session() as session:
        async with session.begin():
            book_repo = BookRepository(session)
            return await book_repo.create_book(name, author, release_year)


@router.get("/books")
async def get_all_books() -> list[Book]:
    async with async_session() as session:
        async with session.begin():
            book_repo = BookRepository(session)
            return await book_repo.get_all_books()


@router.put("/books/{book_id}")
async def update_book(book_id: int, name: str | None = None, author: str | None = None, release_year: str | None = None):
    async with async_session() as session:
        async with session.begin():
            book_repo = BookRepository(session)
            return await book_repo.update_book(book_id, name, author, release_year)


@router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    async with async_session() as session:
        async with session.begin():
            book_repo = BookRepository(session)
            return await book_repo.delete_book(book_id)


@router.post("/users-test")
async def register_user(username: str, password: str, full_name: str):
    async with async_session() as session:
        async with session.begin():
            user_repo = UserRepository(session)
            return await user_repo.create_user(username, password, full_name)


@router.post("/address-test")
async def add_user_address(user_id: int, address: str):
    async with async_session() as session:
        async with session.begin():
            address_repo = AddressRepository(session)
            return await address_repo.create_address(user_id, address)


@router.get("/users-test")
async def get_user_by_username(username: str):
    async with async_session() as session:
        async with session.begin():
            user_repo = UserRepository(session)
            return await user_repo.get_user_by_username(username)