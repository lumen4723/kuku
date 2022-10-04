from option import *
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from utils.exception import *
from datetime import datetime
from user.database import User
from board.qna.database import board_qna
    

class board_qna_like(SQLModel, table=True):
    article_id: int = Field(default=None, foreign_key="board_qna.article_id" ,primary_key=True)

    userid: int = Field(default=None, foreign_key="user.uid", primary_key=True)
    userRel: "User" = Relationship(back_populates="qna_likeRel")

    created: datetime = Field(default=datetime.now())
    state: int = Field(default=1)

def like_qna(article_id:int, db: Session) -> Result:
    try:
        article = db.query(board_qna).filter_by(article_id = article_id).first()
        article.like += 1
        db.add(article)
        db.commit()
        return Ok(article)
    except Exception as e:
        return Err("like qna error")

#dislike board_qna
def dislike_qna(article_id:int, db: Session) -> Result:
    try:
        article = db.query(board_qna).filter_by(article_id = article_id).first()
        if article.like > 0:
            article.like -= 1
            db.add(article)
            db.commit()
            return Ok(article)
        else:
            return Err("dislike qna error")
    except Exception as e:
        return Err("dislike qna error")

# create board_qna_like
def create_qna_like(article_id:int,userid:int, db: Session) -> Result:
    try:
        if db.query(board_qna_like).filter_by(article_id = article_id, userid = userid,state = 1).first() is not None:
            return Err(AlreadyExists())
        check = db.query(board_qna_like).filter_by(article_id = article_id, userid = userid,state = 0).first()
        if check is not None:
            like_qna(article_id, db).unwrap()
            check
            check.state = 1
            db.add(check)
            db.commit()
            return Ok(check)
        like_qna(article_id, db).unwrap()
        article = board_qna_like()
        article.article_id = article_id
        article.userid = userid
        db.add(article)
        db.commit()
        db.refresh(article)
        like_qna(article_id, db).unwrap()
        return Ok(article)
    except Exception as e:
        err_msg = str(e).lower()
        if "duplicate" in err_msg:
            return Err(AlreadyExists())
        elif "like qna error" in err_msg:
            return Err(DefaultException(detail = "like qna error"))
        else:
            dislike_qna(article_id, db)
            return Err(DefaultException(detail = "create qna like error"))

# create cancel qna like
def cancel_qna_like(article_id:int,userid:int, db: Session) -> Result:
    try:
        article = db.query(board_qna_like).filter_by(article_id = article_id, userid = userid, state = 1).first()
        if article is None:
            return Err(NotFound())
        dislike_qna(article_id, db)
        article.state = 0
        db.add(article)
        db.commit()
        return Ok(article)
    except Exception as e:
        err_msg = str(e).lower()
        if "dislike qna error" in err_msg:
            return Err(DefaultException(detail = "dislike qna error"))
        else :
            like_qna(article_id, db)
            return Err(DefaultException(detail = "cancel qna like error"))



