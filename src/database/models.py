from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database.db import Base


class Person(Base):
    __tablename__ = "people"
    __table_args__ = {'schema': 'public'} 

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    info = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    review = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
