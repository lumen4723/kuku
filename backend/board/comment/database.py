from option import *
from pydantic import EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from utils.exception import *
from user.database import User


class board_comment(SQLModel, table=True):
    comment_id: Optional[int] = Field(default=None, primary_key=True)
    content: str

    article_id: int = Field(default=None, foreign_key="board_free.article_id")
    userid: int = Field(default=None, foreign_key="user.uid")
    userRel: "User" = Relationship(back_populates="commentRel")

    created: datetime = Field(default=datetime.now())
    state: int = Field(default=1)  # deleted = 0, normal = 1


def _combine_username(articles: List["board_comment"]) -> Dict:
    # if articles is board_free, then add username
    if type(articles) is board_comment:
        return {
            "comment_id": articles.comment_id,
            "content": articles.content,
            "article_id": articles.article_id,
            "userid": articles.userid,
            "username": articles.userRel.username,
            "created": articles.created,
            "state": articles.state,
        }

    result = []

    for article in articles:
        a = article.dict()
        a["username"] = article.userRel.username

        result.append(a)

    return result


def create_comment(object_in: board_comment, aid: int, uid: int, db: Session) -> Result:
    try:
        comment = board_comment.from_orm(object_in)
        comment.article_id = aid
        comment.userid = uid
        db.add(comment)
        db.refresh(comment)
        return Ok(comment)

    except Exception as e:
        err_msg = str(e).lower()
        if "data too long" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "foreign key constraint fails" in err_msg:
            return Err(DefaultException(detail="user id is not a valid"))
        return Err(DefaultException(detail="unknown error"))


def get_comment(aid: int, db: Session, all: bool = False, page=1, limit=20) -> Result:
    try:
        list = []
        if all:
            list = _combine_username(
                db.query(board_comment).filter(board_comment.article_id == aid).all()
            )
        else:
            list = _combine_username(
                db.query(board_comment)
                .filter(board_comment.article_id == aid)
                .offset((page - 1) * limit)
                .limit(limit)
                .all()
            )
        return Ok(list)

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))
