from sqlalchemy.orm import Session

from .. import schemas
from ..models import models


async def get_all_books(db: Session):
    books = db.query(models.Book).all()
    return books


async def create_book(db: Session, book: schemas.Book, user: schemas.User):
    print(user.username)
    db_book = models.Book(author=book.author, title=book.title, owner_id=user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book