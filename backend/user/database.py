from option import *
from pydantic import EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from .securiy import get_password_hash, verify_password
from utils.exception import *
from .schemas import loginuser, UserInformation


class User(SQLModel, table=True):
    uid: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column_kwargs={"name": "username", "unique": True})
    password: str
    email: EmailStr = Field(sa_column_kwargs={"name": "email", "unique": True})
    created: datetime = Field(default=datetime.now())
    type: int = Field(
        default=0
    )  # emailuncormfirmed = 0, emailconformed = 1,  upser = 2
    state: int = Field(default=1)  # deleted = 0, normal = 1
    
    # board_free <-> user table
    free: List["board_free"] = Relationship(back_populates="userRel")


# get user by email
def get_user_by_email(email: str, db: Session):
    return db.query(User).filter_by(email=email).first()


# get user by uid
def get_user_by_uid(uid: int, db: Session)-> Result:
    user = db.query(User).filter_by(uid=uid).first()
    if user is not None:
        return Ok(UserInformation(username = user.username, email = user.email, created=user.created))
    else:
        return Err(NotFound())


# create_user
def create_user(object_in: User, db: Session) -> Result:
    try:
        object_in.password = get_password_hash(object_in.password)
        user = User.from_orm(object_in)
        db.add(user)
        db.commit()
        db.refresh(user)
        return Ok(
            UserInformation(username = user.username, email = user.email, created=user.created)
        ) 

    except Exception as e:
        err_msg = str(e).lower()

        if "username_unique" in err_msg:
            return Err(AlreadyExists())
        if "email_unique" in err_msg:
            return Err(AlreadyExists())
        if "data too long" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        if "is not a valid" in err_msg:
            return Err(DefaultException(detail="form data is not a valid"))
        return Err(DefaultException(detail="unknown error"))


# get all user objects
def get_all_user(db: Session):
    return db.query(User).all()


# login
def login(object_in: loginuser, db: Session) -> Result:

    user = db.query(User).filter_by(username=object_in.username).first()
    if user is None:
        return Err(NotFound())
    if not verify_password(object_in.password, user.password):
        return Err(NotFound())
    return Ok(user.uid)
