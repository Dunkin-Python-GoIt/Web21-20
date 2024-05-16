from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..schemas import ResponseBook
from ..dependecies import get_token_header
from ..database import get_db
from ..repository.book_model import Book
from ..repository import book_repo


router = APIRouter(prefix="/books", tags=["books"])


@router.get("/{book_id}", response_model=ResponseBook)
async def get_book(
    book_id: Annotated[int, Path(title="The id of book to get")],
    db: Session = Depends(get_db)
    ):
    book = db.get_one(Book, book_id)
    if book:
        print(book)
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/", response_model=list[ResponseBook])
async def all_books(db: Session = Depends(get_db),
    author: Annotated[str | None, Query(alias="author", example="author=Duma")] = None,
    title: Annotated[str | None, Query(alias="title")] = None) -> list[ResponseBook]:
    # if author:
    #     return [book for book in list_of_books if book.author == author]
        # return [book for book in fake_books if book["author"] == author]
    # if title:
        # return [book for book in fake_books if title in book["title"]]
    result = await book_repo.get_all_books(db)
    # db_list_of_books = [Book.model_validate(item) for item in result]
    return result


@router.post("/")
async def add_new_book(
    book: ResponseBook,
    db: Session = Depends(get_db)):
    book = Book(**book.model_dump())
    try:
        db.add(book)
        db.commit()
        db.refresh(book)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=repr(e))
    return book


@router.delete("/{book_id}")
async def delete_book(
    book_id: Annotated[int, Path(title="The id of book to get")],
    db: Session = Depends(get_db)
    ):
    book = db.get_one(Book, book_id)
    db.delete(book)
    db.commit()
    return {"status": f"deleted {book_id}"}

