from option import *
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from utils.exception import *
from typing import TYPE_CHECKING, List

if TYPE_CHECKING: 
    from board.tag_qna.database import board_qna_tag

class tag(SQLModel, table=True):
    tid: Optional[int] = Field(default=None, primary_key=True)
    name : str = Field(sa_column_kwargs={"name": "name", "unique": True})
    slug : str = Field(sa_column_kwargs={"name": "slug", "unique": True})
    color : Optional[str] = Field(default=None)

    tag_qnaRel : List["board_qna_tag"] = Relationship(back_populates="tagRel")



# create tag object
def create_tag(object_in: tag, db: Session) -> Result:
    try:
        tag_object=  tag.from_orm(object_in)
        db.add(tag_object)
        db.commit()
        db.refresh(tag_object)
        return Ok(tag_object)
    except Exception as e:
        err_msg = str(e)
        if "UNIQUE constraint failed" in err_msg:
            return Err(AlreadyExists())
        return Err(DefaultException(detail = "unknown error"))

# get all tags
def get_all_tags(db: Session) -> Result:
    try:
        return Ok(db.query(tag).all())
    except Exception as e:
        return Err(DefaultException(detail = "unknown error"))

# get id by slug
def get_id_by_slug(slug: str, db: Session) -> Result:
    try:
        obj = db.query(tag).filter(tag.slug == slug).first().tid
        return Ok(obj)
    except Exception as e:
        return Err("get id by slug error")