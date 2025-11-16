# from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
# from sqlalchemy.orm import declarative_base, sessionmaker
# from config import DB_URL
# from sqlalchemy import MetaData
# # Base = declarative_base()
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base(metadata=MetaData(schema="public"))


# class Person(Base):
#     __tablename__ = "people"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), unique=True, nullable=False)
#     info = Column(Text, nullable=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

# class Comment(Base):
#     __tablename__ = "comments"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False)
#     comment = Column(Text, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

# class Review(Base):
#     __tablename__ = "reviews"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False)
#     review = Column(Text, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

# # Настройка подключения
# engine = create_engine(DB_URL)
# SessionLocal = sessionmaker(bind=engine)
# Base.metadata.create_all(bind=engine)

# # =============================
# # Функции для работы с базой
# # =============================

# async def add_person(name, info):
#     session = SessionLocal()
#     try:
#         person = session.query(Person).filter_by(name=name).first()
#         if person:
#             # Добавляем новую информацию к старой
#             person.info = (person.info or "") + "\n" + info
#         else:
#             person = Person(name=name, info=info)
#             session.add(person)
#         session.commit()
#     finally:
#         session.close()

# async def get_all_names_from_db():
#     session = SessionLocal()
#     try:
#         return [p.name for p in session.query(Person).all()]
#     finally:
#         session.close()

# async def get_all_comments_from_db():
#     session = SessionLocal()
#     try:
#         comments = session.query(Comment).all()
#         return [f"{c.name}: {c.comment}" for c in comments]
#     finally:
#         session.close()

# async def get_all_reviews_from_db():
#     session = SessionLocal()
#     try:
#         reviews = session.query(Review).all()
#         return [f"{r.name}: {r.review}" for r in reviews]
#     finally:
#         session.close()
