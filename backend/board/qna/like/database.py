from option import *
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from utils.exception import *
from datetime import datetime
from user.database import User
from board.qna.database import board_qna


class board_qna_like(SQLModel, table=True):
    article_id: int = Field(
        default=None, foreign_key="board_qna.article_id", primary_key=True
    )

    userid: int = Field(default=None, foreign_key="user.uid", primary_key=True)
    userRel: "User" = Relationship(back_populates="qna_likeRel")

    created: datetime = Field(default=datetime.now())
    state: int = Field(default=1)


def _like_qna(article_id: int, db: Session, commit: bool = True) -> Result[None, str]:
    try:
        article = db.query(board_qna).filter_by(article_id=article_id).first()
        article.like += 1
        db.add(article)

        if commit:
            db.commit()

        return Ok(None)

    except Exception as e:
        return Err("like qna error")


# dislike board_qna
def _dislike_qna(article_id: int, db: Session, commit: bool = True) -> Result:
    try:
        count = (
            db.query(board_qna)
            .filter_by(article_id=article_id)
            .filter(board_qna.like > 0)
            .update({"like": board_qna.like - 1})
        )

        if commit:
            db.commit()

        if count == 1:
            return Ok(None)

        return Err("dislike_free error")

    except Exception as e:
        return Err("dislike_free error")


# create board_qna_like
def create_qna_like(article_id: int, userid: int, db: Session) -> Result:
    try:
        is_user_already_like = (
            db.query(board_qna_like)
            .filter_by(article_id=article_id, userid=userid, state=1)
            .count()
            > 0
        )

        if is_user_already_like:
            return Err(AlreadyExists())

        _like_qna(article_id, db, commit=False).unwrap()

        is_user_liked_before = (
            db.query(board_qna_like)
            .filter_by(article_id=article_id, userid=userid, state=0)
            .count()
            > 0
        )

        if is_user_liked_before:
            is_state_change_success = (
                db.query(board_qna_like)
                .filter_by(article_id=article_id, userid=userid, state=0)
                .update({board_qna_like.state: 1})
                == 1
            )

            if is_state_change_success is False:
                return Err("state change error")

        else:
            like = board_qna_like()
            like.article_id = article_id
            like.userid = userid
            db.add(like)

        db.commit()
        return Ok(None)

    except Exception as e:
        err_msg = str(e).lower()
        if "duplicate" in err_msg:
            return Err(AlreadyExists())
        elif "like qna error" in err_msg:
            return Err(DefaultException(detail="like qna error"))

        return Err(DefaultException(detail="create qna like error"))


# create cancel qna like
def cancel_qna_like(
    article_id: int, userid: int, db: Session
) -> Result[None, HTTPException]:
    try:
        update_and_check_success = (
            db.query(board_qna_like)
            .filter_by(article_id=article_id, userid=userid, state=1)
            .update({board_qna_like.state: 0})
            == 1
        )

        if update_and_check_success is False:
            return Err(NotFound())

        _dislike_qna(article_id, db, commit=False).unwrap()

        db.commit()
        return Ok(None)

    except Exception as e:
        err_msg = str(e).lower()
        if "dislike qna error" in err_msg:
            return Err(DefaultException(detail="dislike qna error"))

        return Err(DefaultException(detail="cancel qna like error"))
