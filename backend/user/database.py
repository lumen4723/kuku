from option import *
from pydantic import EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional , List
from .securiy import get_password_hash
from utils.exception import *

Base = declarative_base()

    # board_free <-> user table
    free : List["board_free"] = Relationship(back_populates="userRel")



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(128))


# get user by email
def get_user_by_email(email: str, db: Session):
    return db.query(User).filter_by(email=email).first()
