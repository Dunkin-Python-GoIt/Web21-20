from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Depends, Query
from sqlalchemy.orm import Session

from ..models import models

from ..dependecies import get_token_header
from ..database import get_db
from ..repository import book_repo, auth_repo
from .. import schemas


router = APIRouter(prefix="/books", tags=["books"])


@router.get("/{book_id}", response_model=schemas.Book, dependencies=(Depends(auth_repo.get_current_user),))
async def get_book(
    book_id: Annotated[int, Path(title="The id of book to get")],
    db: Session = Depends(get_db)
    ):
    book = db.get_one(models.Book, book_id)
    if book:
        print(book)
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/", response_model=list[schemas.Book], dependencies=(Depends(auth_repo.get_current_user),))
async def all_books(db: Session = Depends(get_db),
    author: Annotated[str | None, Query(alias="author", example="author=Duma")] = None,
    title: Annotated[str | None, Query(alias="title")] = None) -> list[schemas.Book]:
    result = await book_repo.get_all_books(db)
    return result


@router.post("/", response_model=schemas.Book)
async def add_new_book(
    book: schemas.BookBase,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth_repo.get_current_user)):
    
    book = await book_repo.create_book(db, book, user)
    return book


@router.delete("/{book_id}")
async def delete_book(
    book_id: Annotated[int, Path(title="The id of book to get")],
    db: Session = Depends(get_db)
    ):
    book = db.get_one(models.Book, book_id)
    db.delete(book)
    db.commit()
    return {"status": f"deleted {book_id}"}

