from database.db import SessionLocal
from sqlalchemy.orm import Session
from database.models import Person, Comment, Review


def add_person(name, info):
    session = SessionLocal()
    try:
        person = session.query(Person).filter_by(name=name).first()
        if person:
            person.info = (person.info or "") + "\n" + info
        else:
            person = Person(name=name, info=info)
            session.add(person)
        session.commit()
    finally:
        session.close()


def get_all_names():
    session = SessionLocal()
    try:
        return [p.name for p in session.query(Person).all()]
    finally:
        session.close()


def get_all_comments():
    session = SessionLocal()
    try:
        return [f"{c.name}: {c.comment}" for c in session.query(Comment).all()]
    finally:
        session.close()


def get_all_reviews():
    session = SessionLocal()
    try:
        return [f"{r.name}: {r.review}" for r in session.query(Review).all()]
    finally:
        session.close()


def delete_person(name):
    pass

    
def get_all_people(db: Session):
    return db.query(Person).all()
