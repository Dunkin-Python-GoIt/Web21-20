from sqlalchemy.orm import Session

from .book_model import Book



async def get_all_books(db: Session):
    books = db.query(Book).all()
    return books