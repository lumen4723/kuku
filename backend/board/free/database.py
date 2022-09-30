from option import *
from pydantic import EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from utils.exception import *
from user.database import User
from board.information.database import change_information, board_information
from sqlalchemy import desc


class board_free(SQLModel, table=True):
    article_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str

    userid: int = Field(default=None, foreign_key="user.uid")
    userRel: "User" = Relationship(back_populates="free")

    created: datetime = Field(default=datetime.now())
    state: int = Field(default=1)  # deleted = 0, normal = 1
    like: int = Field(default=0)
    views: int = Field(default=0)


def _combine_username(articles: List["board_free"]) -> dict:
    # if articles is board_free, then add username
    if type(articles) is board_free:
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
def create_article(object_in: board_free, uid: int, db: Session) -> Result:
    try:
        article = board_free.from_orm(object_in)
        article.userid = uid
        db.add(article)
        db.commit()
        db.refresh(article)
        change_information("free", 0, db).map_err(throwMsg).unwrap()
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
        article_cnt = db.query(board_information).filter_by(description="free").first()
        if article_cnt is None:
            article_cnt = 0
        else:
            article_cnt = article_cnt.size
        if all:
            return Ok(
                {
                    "list": _combine_username(
                        db.query(board_free)
                        .filter_by(state=1)
                        .order_by(board_free.created.desc())
                        .join(User)
                        .all()
                    ),
                    "cnt": article_cnt,
                }
            )

        start = (page - 1) * limit
        list = _combine_username(
            db.query(board_free)
            .filter_by(state=1)
            .order_by(board_free.created.desc())
            .join(User)
            .offset(start)
            .limit(limit)
            .all()
        )
        article_cnt = db.query(board_information).filter_by(description="free").first()
        if article_cnt is None:
            article_cnt = 0
        else:
            article_cnt = article_cnt.size
        return Ok({"list": list, "cnt": article_cnt,})
    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))

        return Err(DefaultException(detail="unknown error"))


# get ariticle by id from
def get_article_by_id(article_id: int, db: Session):
    try:
        article = _combine_username(
            db.query(board_free)
            .filter_by(article_id=article_id, state=1)
            .order_by(board_free.created.desc())
            .join(User)
            .first()
        )

        # increase views by 1 when get article
        article["views"] += 1
        db.query(board_free).filter_by(article_id=article_id).update(
            {"views": article["views"]}
        )
        db.commit()

        return Ok(article)

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))


# get article by uid form
def get_article_by_uid(uid: int, db: Session):
    try:
        article = _combine_username(
            db.query(board_free)
            .filter_by(userid=uid, state=1)
            .order_by(board_free.created.desc())
            .join(User)
            .all()
        )
        return Ok(article)

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))


# delete article by id
def delete_article(article_id: int, uid: int, db: Session):
    try:
        article = db.query(board_free).filter_by(article_id=article_id, state=1).first()
        if article is None:
            return Err(NotFound())
        elif article.userid != uid:
            return Err(NotAuthorized())
        article.state = 0
        db.add(article)
        db.commit()
        db.refresh(article)
        change_information("free", 1, db).map_err(throwMsg).unwrap()
        return Ok(article)

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))


# update article by id
def update_article(article_id: int, uid: int, object_in: board_free, db: Session):
    try:
        article = db.query(board_free).filter_by(article_id=article_id, state=1).first()
        if article is None:
            return Err(NotFound())
        elif article.userid != uid:
            return Err(NotAuthorized())
        article.title = object_in.title
        article.content = object_in.content
        db.add(article)
        db.commit()
        db.refresh(article)
        return Ok(article)

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))
