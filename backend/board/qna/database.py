from option import *
from pydantic import EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from utils.exception import *
from user.database import User


class board_qna(SQLModel, table=True):
    article_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str

    userid: int = Field(default=None, foreign_key="user.uid")
    userRel: "User" = Relationship(back_populates="qna")

    created: datetime = Field(default=datetime.now())
    state: int = Field(default=1)  # deleted = 0, normal = 1
    like: int = Field(default=0)
    views: int = Field(default=0)


def _combine_username(articles: List["board_qna"]) -> dict:
    # if articles is board_free, then add username
    if type(articles) is board_qna:
        return {
            "article_id": articles.article_id,
            "title": articles.title,
            "content": articles.content,
            "userid": articles.userid,
            "username": articles.userRel.username,
            "created": articles.created,
            "state": articles.state,
            "like": articles.like,
            "views": articles.views,
        }

    result = []

    for article in articles:
        a = article.dict()
        a["username"] = article.userRel.username

        result.append(a)

    return result


# create board_free aritcle
def create_article(object_in: board_qna, uid: int, db: Session) -> Result:
    try:
        article = board_qna.from_orm(object_in)
        article.userid = uid
        db.add(article)
        db.commit()
        db.refresh(article)
        return Ok(article)

    except Exception as e:
        err_msg = str(e).lower()
        if "data too long" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "foreign key constraint fails" in err_msg:
            return Err(DefaultException(detail="user id is not a valid"))
        return Err(DefaultException(detail="unknown error"))


def list_article(db: Session, all: bool = False, page=1, limit=20):
    try:
        article_cnt = db.query(board_qna).count()
        if all:
            return Ok(
                {
                    "list": _combine_username(db.query(board_qna).join(User).all()),
                    "cnt": article_cnt,
                }
            )

        start = (page - 1) * limit
        list = _combine_username(
            db.query(board_qna).join(User).offset(start).limit(limit).all()
        )
        article_cnt = db.query(board_qna).count()

        return Ok(
            {
                "list": list,
                "cnt": article_cnt,
            }
        )
    except Exception as e:
        print(e)
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))

        return Err(DefaultException(detail="unknown error"))


# get ariticle by id from
def get_article(article_id: int, db: Session):
    try:
        article = _combine_username(
            db.query(board_qna).filter_by(article_id=article_id).join(User).first()
        )
        return Ok(article)

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))

        return Err(DefaultException(detail="unknown error"))
