from fastapi import APIRouter
from database.config import async_session
from database.repositories import BookRepository
from database.models import Book

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