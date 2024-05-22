from __future__ import annotations

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    author: str = Field(title="Author of the book", min_length=3, max_length=15)
    title: str


class BookCreate(BookBase):
    ...


class Book(BookBase):
    id: int
    title: str
    owner_id: int
    owner: UserBase
    
    class Config:
        from_attributes = True
        

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    
    
class User(UserBase):
    id: int
    books: list[Book] = []
    
    class Config:
        from_attributes = True