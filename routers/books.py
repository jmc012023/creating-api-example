from fastapi import APIRouter
from models.book import BookModel
from schemas.books import PartialBook

router = APIRouter(
    prefix="/books"
)

@router.get("/", status_code=200)
async def books():
    books = BookModel.get_all()
    return books

@router.get("/id/", status_code=200)
async def get_book_id(id: int):
    book = BookModel.get_by_id(id)
    return book

@router.get("/isbn/{isbn}", status_code=200)
async def get_books_isbn(isbn: str):
    books = BookModel.get_by_isbn(isbn)
    return books

@router.get("/title/{title}", status_code=200)
async def get_books_title(title: str):
    books = BookModel.get_by_title(title)
    return books

@router.post("/", status_code=201)
async def new_book(book: PartialBook):
    new_book = BookModel.create(book)
    return new_book

@router.patch("/update/")
async def update_book(id: int, title: str):
    updated_book = BookModel.update_title(id, title)
    return updated_book

@router.delete("/")
async def delete_book(id: int):
    return BookModel.delete(id)