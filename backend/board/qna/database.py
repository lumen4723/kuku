from option import *
from datetime import datetime
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from utils.exception import *
from user.database import User
from .schemas import Board_qna_question, Board_qna_answer
from board.information.database import change_information, board_information
from board.tag_qna.database import *
from board.tag.database import *


class board_qna(SQLModel, table=True):
    article_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str

    userid: int = Field(default=None, foreign_key="user.uid")
    userRel: "User" = Relationship(back_populates="qna")

    created: datetime = Field(default=datetime.now())
    state: int = Field(default=1)  # deleted = 0, normal = 1
    is_clear: int = Field(default=0)  # notCleared = 0, cleared = 1

    parentid: Optional[int] = Field(default=None, foreign_key="board_qna.article_id")
    views: int = Field(default=0)
    like: int = Field(default=0)

    tagRel: List["board_qna_tag"] = Relationship(back_populates="boardRel")


def _combine_username_tags(articles: List["board_qna"]) -> Dict:
    # if articles is board_free, then add username
    tagList = []
    if type(articles) is board_qna:
        for getTag in articles.tagRel:
            tagList.append(getTag.tagRel)
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
            "tags": tagList,
        }
    result = []
    for article in articles:
        a = article.dict()
        a["username"] = article.userRel.username
        for getTag in article.tagRel:
            tagList.append(getTag.tagRel)
        a["tags"] = tagList
        tagList = []
        result.append(a)
    return result


# create board_free aritcle
def create_question(object_in: Board_qna_question, uid: int, db: Session) -> Result:
    try:
        article = board_qna()
        article.title = object_in.title
        article.content = object_in.content
        article.userid = uid
        db.add(article)
        db.commit()
        change_information("qna", True, db, commit=False)
        for tag in object_in.tags:
            tagid = get_id_by_slug(tag, db).unwrap()
            create_tag_qna(article.article_id, tagid, db, commit=False).unwrap()

        db.commit()
        db.refresh(article)

        return Ok(article)
    except Exception as e:
        err_msg = str(e).lower()
        if "data too long" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "foreign key constraint fails" in err_msg:
            return Err(DefaultException(detail="user id is not a valid"))
        elif "change information error" in err_msg:
            return Err(DefaultException(detail="change information error"))
        elif "get id by slug error" in err_msg:
            return Err(DefaultException(detail="get id by slug error"))
        elif "create tag qna error" in err_msg:
            return Err(DefaultException(detail="create tag qna error"))
        return Err(DefaultException(detail=err_msg))


# create board_qna answer
def create_answer(object_in: Board_qna_answer, uid: int, db: Session) -> Result:
    try:
        article = board_qna()
        article.title = object_in.title
        article.content = object_in.content
        article.userid = uid
        article.parentid = object_in.parentid

        db.add(article)
        change_information("qna", True, db, commit=False)

        db.commit()
        db.refresh(article)

        return Ok(article)

    except Exception as e:
        err_msg = str(e).lower()
        if "data too long" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "foreign key constraint fails" in err_msg:
            return Err(DefaultException(detail="user id is not a valid"))
        elif "change information error" in err_msg:
            return Err(DefaultException(detail="change information error"))

        return Err(DefaultException(detail=err_msg))


# update board_qna answer
def update_answer(
    object_in: Board_qna_answer, aid: int, uid: int, db: Session
) -> Result:
    try:
        article = db.query(board_qna).filter_by(article_id=aid).first()
        if article.userid != uid:
            return Err(
                DefaultException(detail="you are not the author of this article")
            )
        article.title = object_in.title
        article.content = object_in.content
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
        return Err(DefaultException(detail=err_msg))


# delete board_qna aritcle
def delete_article(
    article_id: int, uid: int, db: Session
) -> Result[None, HTTPException]:
    try:
        article = db.query(board_qna).filter_by(article_id=article_id).first()
        if article is None:
            return Err(NotFound())
        if article.userid != uid:
            return Err(NotAuthorized())

        article.state = 0
        db.add(article)

        change_information("qna", False, db, commit=False)

        db.commit()
        db.refresh(article)
        return Ok(None)

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "change information error" in err_msg:
            return Err(DefaultException(detail="change information error"))
        elif "nonetype" in err_msg:
            return Err(NotFound())

        return Err(DefaultException(detail="unknown error"))


def list_article(
    db: Session, all: bool = False, aid=-1, page=1, limit=20, like: bool = False
) -> Result:
    try:
        article_cnt = db.query(board_information).filter_by(description="qna").first()
        order = board_qna.like.desc() if like else None
        if all:
            return Ok(
                {
                    "list": _combine_username_tags(
                        db.query(board_qna)
                        .filter_by(state=1, parentid=None)
                        .order_by(order, board_qna.created.desc())
                        .all()
                    ),
                    "cnt": article_cnt.size,
                }
            )

        start = (page - 1) * limit
        list = _combine_username_tags(
            db.query(board_qna)
            .filter_by(state=1, parentid=(None if aid == -1 else aid))
            .join(User)
            .order_by(order, board_qna.created.desc())
            .offset(start)
            .limit(limit)
            .all()
        )
        article_cnt = db.query(board_information).filter_by(description="qna").first()

        return Ok({"list": list, "cnt": article_cnt.size,})
    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))


def _combine_username_tags_slug(articles: list) -> list:
    # if articles is board_free, then add username
    result = []
    tagList = []
    for article in articles:
        a = article.board_qna.dict()
        a["username"] = article.board_qna.userRel.username
        for getTag in article.board_qna.tagRel:
            tagList.append(getTag.tagRel)
        a["tags"] = tagList
        result.append(a)
        tagList = []
    return result


def list_article_by_slug(
    db: Session, slug: str, all: bool = False, page=1, limit=20, like=False
) -> Result:
    try:
        # 성능 저하가 있다고 해도 이렇게 하는게 좋을듯 합니다. information으로 tag 관리를 하기에는 너무 복잡해질 것 같아서요.
        count = (
            db.query(tag)
            .filter_by(slug=slug)
            .join(board_qna_tag)
            .join(board_qna)
            .filter(board_qna.state == 1)
            .count()
        )
        qurey = (
            db.query(tag, board_qna_tag, board_qna)
            .filter(tag.slug == slug)
            .join(board_qna_tag, tag.tid == board_qna_tag.tagid)
            .join(board_qna, board_qna_tag.article_id == board_qna.article_id)
            .filter(board_qna.state == 1)
        )
        order = board_qna.like.desc() if like else None
        if all:
            return Ok(
                {
                    "list": _combine_username_tags_slug(
                        qurey.order_by(order, board_qna.created.desc()).all()
                    ),
                    "cnt": count,
                }
            )

        start = (page - 1) * limit
        return Ok(
            {
                "list": _combine_username_tags_slug(
                    qurey.order_by(order, board_qna.created.desc())
                    .offset(start)
                    .limit(limit)
                    .all()
                ),
                "cnt": count,
            }
        )

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))


# get ariticle by id from
def get_article(article_id: int, db: Session) -> Result:
    try:
        article = (
            db.query(board_qna)
            .filter_by(article_id=article_id, state=1)
            .join(User)
            .first()
        )
        article.views += 1
        db.add(article)
        db.commit()

        article = _combine_username_tags(article)
        answers = _combine_username_tags(
            db.query(board_qna)
            .filter_by(parentid=article_id, state=1)
            .join(User)
            .order_by(board_qna.like.desc())
            .all()
        )
        article["answers"] = answers
        return Ok(article)

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))


# update ariticle
def update_article(
    object_in: Board_qna_question, article_id: int, uid: int, db: Session
) -> Result:
    try:
        article = db.query(board_qna).filter_by(article_id=article_id, state=1).first()
        if article is None:
            return Err(NotFound())
        elif article.userid != uid:
            return Err(NotAuthorized())

        article.title = object_in.title
        article.content = object_in.content
        db.add(article)

        delete_all_tag_qna(article_id, db, commit=False).unwrap()

        for getTag in object_in.tags:
            tagid = get_id_by_slug(getTag, db).unwrap()
            create_tag_qna(article_id, tagid, db, commit=False).unwrap()

        db.commit()
        db.refresh(article)

        return Ok(article)

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "delete_all_tag_qna error" in err_msg:
            return Err(DefaultException(detail="delete_all_tag_qna error"))
        elif "get id by slug error" in err_msg:
            return Err(DefaultException(detail="get id by slug error"))
        elif "create tag qna error" in err_msg:
            return Err(DefaultException(detail="create tag qna error"))
        return Err(DefaultException(detail="unknown error"))


# board_qna is_clear is sucessful
def clear_article(article_id: int, uid: int, db: Session) -> Result:
    try:
        article = db.query(board_qna).filter_by(article_id=article_id, state=1).first()
        if article is None:
            return Err(NotFound())
        elif article.userid != uid:
            return Err(NotAuthorized())
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


# search article by title
def get_article_by_title(findtitle: str, db: Session, page=1, limit=20) -> Result:
    try:
        start = (page - 1) * limit
        article = _combine_username_tags(
            db.query(board_qna)
            .filter_by(state=1)
            .order_by(board_qna.created.desc())
            .join(User)
            .offset(start)
            .limit(limit)
            .all()
        )

        result = []
        cnt = 0
        for a in article:
            if findtitle in a["title"]:
                result.append(a)
                cnt += 1

        return Ok({"list": result, "cnt": cnt})

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))


# search article by username
def get_article_by_username(finduser: str, db: Session, page=1, limit=20) -> Result:
    try:
        start = (page - 1) * limit
        article = _combine_username_tags(
            db.query(board_qna)
            .filter_by(state=1)
            .order_by(board_qna.created.desc())
            .join(User)
            .offset(start)
            .limit(limit)
            .all()
        )

        result = []
        cnt = 0
        for a in article:
            if finduser in a["username"]:
                result.append(a)
                cnt += 1

        return Ok({"list": result, "cnt": cnt})

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))


# search article by content
def get_article_by_content(findcontent: str, db: Session, page=1, limit=20) -> Result:
    try:
        start = (page - 1) * limit
        article = _combine_username_tags(
            db.query(board_qna)
            .filter_by(state=1)
            .order_by(board_qna.created.desc())
            .join(User)
            .offset(start)
            .limit(limit)
            .all()
        )

        result = []
        cnt = 0
        for a in article:
            if findcontent in a["content"]:
                result.append(a)
                cnt += 1

        return Ok({"list": result, "cnt": cnt})

    except Exception as e:
        err_msg = str(e).lower()
        if "background" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        elif "nonetype" in err_msg:
            return Err(NotFound())
        return Err(DefaultException(detail="unknown error"))

