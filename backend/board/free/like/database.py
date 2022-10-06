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


def _like_free(article_id: int, db: Session, commit: bool = True) -> Result:
    try:
        article = (
            db.query(board_free)
            .filter_by(article_id=article_id)
            .update({"like": board_free.like + 1})
        )

        if commit:
            db.commit()

        return Ok(article)
    except Exception as e:
        return Err("like_free error")


# dislike board_free
def _dislike_free(
    article_id: int, db: Session, commit: bool = True
) -> Result[None, str]:
    try:
        article = (
            db.query(board_free)
            .filter_by(article_id=article_id)
            .filter(board_free.like > 0)
            .update({"like": board_free.like - 1})
        )

        if commit:
            db.commit()

        if article == 1:
            return Ok(None)
        else:
            return Err("dislike_free error")

    except Exception as e:
        return Err("dislike_free error")


# create board_free_like
def create_free_like(article_id: int, userid: int, db: Session) -> Result[None, Any]:
    try:
        is_user_already_like = (
            db.query(board_free_like)
            .filter_by(article_id=article_id, userid=userid, state=1)
            .count()
            > 0
        )

        if is_user_already_like:
            return Err(AlreadyExists())

        if _like_free(article_id, db, commit=False).is_err:
            return Err("like_free error")

        is_user_liked_before = (
            db.query(board_free_like)
            .filter_by(article_id=article_id, userid=userid, state=0)
            .count()
            > 0
        )

        if is_user_liked_before:
            is_state_change_success = (
                db.query(board_free_like)
                .filter_by(article_id=article_id, userid=userid, state=0)
                .update({board_free_like.state: 1})
                == 1
            )

            if is_state_change_success is False:
                return Err("state change error")
        else:
            article = board_free_like()
            article.article_id = article_id
            article.userid = userid
            db.add(article)

        db.commit()
        return Ok(None)

    except Exception as e:
        err_msg = str(e).lower()
        if "duplicate" in err_msg:
            return Err(AlreadyExists())
        elif "like_free error" in err_msg:
            return Err(DefaultException(detail="like_free error"))

        return Err(DefaultException(detail="create_free like error"))


# create cancel_free like
def cancel_free_like(article_id: int, userid: int, db: Session) -> Result[None, Any]:
    try:
        update_and_check_success = (
            db.query(board_free_like)
            .filter_by(article_id=article_id, userid=userid, state=1)
            .update({board_free_like.state: 0})
            == 1
        )

        if update_and_check_success == False:
            return Err(NotFound())

        if _dislike_free(article_id, db, commit=False).is_err:
            return Err("dislike_free error")

        db.commit()
        return Ok(None)
    except Exception as e:
        err_msg = str(e).lower()
        if "dislike_free error" in err_msg:
            return Err(DefaultException(detail="dislike_free error"))

        return Err(DefaultException(detail="cancel_free like error"))
