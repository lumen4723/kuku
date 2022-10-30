from option import *
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from utils.exception import *


# lecture -> course_id, title, slug, description
class lecture(SQLModel, table=True):
    course_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    slug: str
    description: str
    articleRel: "lecture_article" = Relationship(back_populates="lectureRel")


# lecture_article -> no, title, content, category, parent_id (null), course_id
class lecture_article(SQLModel, table=True):
    no: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    parent_id: Optional[int] = Field(default=None)
    course_id: int = Field(default=None, foreign_key="lecture.course_id")
    lectureRel: "lecture" = Relationship(back_populates="articleRel")
    exampleCodeRel: "lecture_example_code" = Relationship(
        back_populates="lecture_articleRel"
    )


# lecture_example_code -> no, lecture_article_id, language, code
class lecture_example_code(SQLModel, table=True):
    no: Optional[int] = Field(default=None, primary_key=True)
    lecture_article_id: int = Field(default=None, foreign_key="lecture_article.no")
    lecture_articleRel: "lecture_article" = Relationship(
        back_populates="exampleCodeRel"
    )
    language: str
    code: str


### CRUD 순서대로 작성함
### 단일 Row를 가져오는건 get, 여러 Row를 가져오는건 list


def list_course(db: Session):
    try:
        return Ok(db.query(lecture).all())
    except Exception as e:
        return Err(str(e))


def list_chapter(course: str, db: Session):
    try:
        # get course id from lecture
        course_data = db.query(lecture).filter(lecture.slug == course).first()
        if course_data is None:  
            return Err("Course not found")

        course_id = course_data.course_id

        # get chapter list from lecture_article
        return Ok(
            db.query(lecture_article)
            .filter(lecture_article.course_id == course_id)
            .all()
        )

    except Exception as e:
        return Err(str(e))


def get_chapter_example_code(course: str, chapter: int, db: Session):
    try:
        # get course id from lecture
        course_id = db.query(lecture).filter(lecture.slug == course).first().course_id

        # get chapter list from lecture_article
        return Ok(
            db.query(lecture_example_code)
            .filter(lecture_example_code.lecture_article_id == chapter)
            .all()
        )

    except Exception as e:
        return Err(str(e))
