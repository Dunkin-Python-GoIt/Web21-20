from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..dependecies import get_token_header
from ..database import get_db
from ..models.book import Book as Book_db


router = APIRouter()


class ResponseBook(BaseModel):
    id: int
    author: str = Field(title="Author of the book", min_length=3, max_length=15)
    title: str
    
    class Config:
        orm_mode = True


fake_books = [
        {
            "id": 1,
            "author": "Duma", 
            "title": "3 Mushkiters"
            },
        {
            "id": 2,
            "author": "Gerbert",
            "title": "Duna"
        },
        {
            "id": 3,
            "author": "Duma",
            "title": "The Count of Monte Cristo"
        }
        ]

list_of_books = [ResponseBook.model_validate(book) for book in fake_books]


@router.get("/books/{book_id}", dependencies=[Depends(get_token_header)])
async def get_book(book_id: Annotated[int, Path(title="The id of book to get")]):
    for book in fake_books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/books/", response_model=list[ResponseBook])
async def all_books(db: Session = Depends(get_db),
    author: Annotated[str | None, Query(alias="author", example="author=Duma")] = None,
    title: Annotated[str | None, Query(alias="title")] = None) -> list[ResponseBook]:
    if author:
        return [book for book in list_of_books if book.author == author]
        # return [book for book in fake_books if book["author"] == author]
    # if title:
        # return [book for book in fake_books if title in book["title"]]
    result = db.query(Book_db).all()
    print(result)
    # db_list_of_books = [Book.model_validate(item) for item in result]
    return result


@router.post("/books/")
async def add_new_book(book: ResponseBook):
    fake_books.append(book)
    return fake_books