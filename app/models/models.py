from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base, engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    
    books = relationship("Book", back_populates="owner")


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    author = Column(String)
    title = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="books")
    

Base.metadata.create_all(bind=engine)