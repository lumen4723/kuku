from option import *
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(128))


# get user by email
def get_user_by_email(email: str, db: Session):
    return db.query(User).filter_by(email=email).first()
