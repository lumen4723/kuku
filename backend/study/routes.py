### 전체적인 구조: 여러개의 코스 (알고리즘, 그래픽스, 컴퓨터구조) -> 여러개의 챕터 (Brute Force, Sorting)


from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from utils.session import *
from board.free.like.database import *
from board.free.comment.database import *

router = APIRouter(
    prefix="/study",
    tags=["study"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list_all_course(session: Session = Depends(utils.database.get_db)):
    return database.list_course(session).map_err(throwMsg).unwrap()


@router.get("/head-chapters")
async def list_head_chapter(session: Session = Depends(utils.database.get_db)):
    def flatten_course(article: List[database.lecture_article]):
        return tuple(
            map(
                lambda x: {
                    "no": x.no,
                    "title": x.title,
                    "content": x.content,
                    "category": x.category,
                    "parent_id": x.parent_id,
                    "course_id": x.course_id,
                    "course_title": x.lectureRel.title,
                    "course_slug": x.lectureRel.slug,
                },
                article,
            )
        )

    return (
        database.list_head_chapter(session)
        .map(flatten_course)
        .map_err(throwMsg)
        .unwrap()
    )


@router.get("/{course}/list")
async def list_course_chapter(
    course: str, session: Session = Depends(utils.database.get_db)
):
    class course_tree:
        no: Optional[int]
        title: str
        content: str
        category: str
        parent_id: Optional[int]
        children: List["course_tree"]

        def __init__(self, data: database.lecture_article):
            self.no = data.no
            self.title = data.title
            self.content = data.content
            self.category = data.category
            self.parent_id = data.parent_id
            self.children = []

    chapters = database.list_chapter(course, session).map_err(throwMsg).unwrap()
    chapater_dict = {}

    for chapter in chapters:
        chapater_dict[chapter.no] = course_tree(chapter)

    chapter_list = []
    for (idx, chapter) in chapater_dict.items():
        if chapter.parent_id == None:
            chapter_list.append(chapter)
        else:
            chapater_dict[chapter.parent_id].children.append(chapter)

    return chapter_list


@router.get("/{course}/{chapter}/")
async def list_chapter_lecture(
    course: str, chapter: str, session: Session = Depends(utils.database.get_db)
):
    pass
