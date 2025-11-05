from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from db import Base

class Name(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    info = Column(Text, default="")
    private_comments = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(String(100))
    username = Column(String(200))
    text = Column(Text)
    photo_file_id = Column(String(400))
    created_at = Column(DateTime, default=datetime.utcnow)
    visible_to_guests = Column(Boolean, default=True)
