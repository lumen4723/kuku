from option import *
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from utils.exception import *
from board.tag.database import tag
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board.qna.database import board_qna


class board_qna_tag(SQLModel, table=True):
    article_id: int = Field(
        default=None, foreign_key="board_qna.article_id", primary_key=True
    )
    boardRel: "board_qna" = Relationship(back_populates="tagRel")

    tagid: int = Field(default=None, foreign_key="tag.tid", primary_key=True)
    tagRel: "tag" = Relationship(back_populates="tag_qnaRel")


# create board_tag_qna
def create_tag_qna(
    article_id: int, tagid: int, db: Session, commit: bool = True
) -> Result:
    try:
        tag = board_qna_tag()
        tag.article_id = article_id
        tag.tagid = tagid

        db.add(tag)
        db.refresh(tag)

        if commit:
            db.commit()

        return Ok(tag)
    except Exception as e:
        return Err(DefaultException(detail="create tag qna error"))


# delete board_tag_qna
def delete_tag_qna(
    article_id: int, tagid: int, db: Session, commit: bool = True
) -> Result:
    try:
        article = board_qna_tag()
        article.article_id = article_id
        article.tagid = tagid
        db.delete(article)
        if commit:
            db.commit()

        return Ok(article)
    except Exception as e:
        err_msg = str(e)
        return Err(DefaultException(detail="unknown error"))


# delete all board_tag_qna with article_id
def delete_all_tag_qna(
    article_id: int, db: Session, commit: bool = True
) -> Result[bool, str]:
    try:
        article = (
            db.query(board_qna_tag)
            .filter(board_qna_tag.article_id == article_id)
            .delete()
        )

        if commit:
            db.commit()

        return Ok(article > 0)
    except Exception as e:
        return Err("delete_all_tag_qna error")
