from option import *
from pydantic import EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from utils.exception import *
from user.database import User


class board_free_comment(SQLModel, table=True):
    cid: Optional[int] = Field(default=None, primary_key=True)
    userid: int = Field(default=None, foreign_key="user.uid")
    userRel: "User" = Relationship(back_populates="comment")

    article_id: int = Field(default=None, foreign_key="board_free.article_id")
    content: str

    created: datetime = Field(default=datetime.now())
    state: int = Field(default=1)  # deleted = 0, normal = 1


def _combine_username(comments: List["board_free_comment"]) -> Dict:
    # if comments is board_free, then add username
    if type(comments) is board_free_comment:
        return {
            "cid": comments.cid,
            "userid": comments.userid,
            "username": comments.userRel.username,
            "article_id": comments.article_id,
            "content": comments.content,
            "created": comments.created,
            "state": comments.state,
        }

    result = []

    for comment in comments:
        a = comment.dict()
        a["username"] = comment.userRel.username

        result.append(a)

    return result


def create_free_comment(
    object_in: board_free_comment, aid: int, uid: int, db: Session
) -> Result:
    try:
        comment = board_free_comment.from_orm(object_in)
        comment.article_id = aid
        comment.userid = uid
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return Ok(comment)

    except Exception as e:
        err_msg = str(e).lower()
        if "data too long" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "foreign key constraint fails" in err_msg:
            return Err(DefaultException(detail="user id is not a valid"))
        return Err(DefaultException(detail="unknown error"))


def get_comment(aid: int, db: Session) -> Result:
    try:
        comments = _combine_username(
            db.query(board_free_comment)
            .filter(board_free_comment.article_id == aid, board_free_comment.state == 1)
            .join(User)
            .all()
        )

        return Ok({"list": comments})

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))

#delete comment
def delete_comment(cid: int, uid: int,db: Session) -> Result:
    try:
        comment = db.query(board_free_comment).filter(board_free_comment.cid == cid).first()
        if comment is None:
            return Err(NotFound())
        elif comment.userid != uid: 
            return Err(NotAuthorized())
        comment.state = 0
        db.commit()
        return Ok(comment)

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))
