from sqlalchemy import Column, Integer, String

from ..database import Base, engine


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    author = Column(String)
    title = Column(String)
    

Base.metadata.create_all(bind=engine)