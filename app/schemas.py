from pydantic import BaseModel, Field


class ResponseBook(BaseModel):
    id: int
    author: str = Field(title="Author of the book", min_length=3, max_length=15)
    title: str
    
    class Config:
        orm_mode = True