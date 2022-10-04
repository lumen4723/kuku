from option import *
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from utils.exception import *
from datetime import datetime
from user.database import User
from board.free.database import board_free


class board_free_like(SQLModel, table=True):
    article_id: int = Field(
        default=None, foreign_key="board_free.article_id", primary_key=True
    )

    userid: int = Field(default=None, foreign_key="user.uid", primary_key=True)
    userRel: "User" = Relationship(back_populates="free_likeRel")

    created: datetime = Field(default=datetime.now())
    state: int = Field(default=1)


def like_free(article_id: int, db: Session) -> Result:
    try:
        article = db.query(board_free).filter_by(article_id=article_id).first()
        article.like += 1
        db.add(article)
        db.commit()
        return Ok(article)
    except Exception as e:
        return Err("like_free error")


# dislike board_free
def dislike_free(article_id: int, db: Session) -> Result:
    try:
        article = db.query(board_free).filter_by(article_id=article_id).first()
        if article.like > 0:
            article.like -= 1
            db.add(article)
            db.commit()
            return Ok(article)
        else:
            return Err("dislike_free error")
    except Exception as e:
        return Err("dislike_free error")


# create board_free_like
def create_free_like(article_id: int, userid: int, db: Session) -> Result:
    try:
        if (
            db.query(board_free_like)
            .filter_by(article_id=article_id, userid=userid, state=1)
            .first()
            is not None
        ):
            return Err(AlreadyExists())
        check = (
            db.query(board_free_like)
            .filter_by(article_id=article_id, userid=userid, state=0)
            .first()
        )
        if check is not None:
            like_free(article_id, db).unwrap()
            check
            check.state = 1
            db.add(check)
            db.commit()
            return Ok(check)
        like_free(article_id, db).unwrap()
        article = board_free_like()
        article.article_id = article_id
        article.userid = userid
        db.add(article)
        db.commit()
        db.refresh(article)
        like_free(article_id, db).unwrap()
        return Ok(article)
    except Exception as e:
        err_msg = str(e).lower()
        if "duplicate" in err_msg:
            return Err(AlreadyExists())
        elif "like_free error" in err_msg:
            return Err(DefaultException(detail="like_free error"))
        else:
            dislike_free(article_id, db)
            return Err(DefaultException(detail="create_free like error"))


# create cancel_free like
def cancel_free_like(article_id: int, userid: int, db: Session) -> Result:
    try:
        article = (
            db.query(board_free_like)
            .filter_by(article_id=article_id, userid=userid, state=1)
            .first()
        )
        if article is None:
            return Err(NotFound())
        dislike_free(article_id, db)
        article.state = 0
        db.add(article)
        db.commit()
        return Ok(article)
    except Exception as e:
        err_msg = str(e).lower()
        if "dislike_free error" in err_msg:
            return Err(DefaultException(detail="dislike_free error"))
        else:
            like_free(article_id, db)
            return Err(DefaultException(detail="cancel_free like error"))
