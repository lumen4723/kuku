from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from .schemas import board_comment_create
from utils.session import *

router = APIRouter(
    prefix="/board/comment",
    tags=["board_comment"],
    responses={404: {"description": "Not found"}},
)

# create comment router
@router.post(
    "/comment/create/{article_id}",
    dependencies=[Depends(cookie)],
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    comment: board_comment_create,
    article_id: int,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        database.create_comment(comment, article_id, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


# get comment by article id router
@router.get("/comment/article_id/{article_id}")
async def get_comment_by_article_id(
    article_id: int, session: Session = Depends(utils.database.get_db)
):
    return database.get_comment(article_id, session).map_err(throwMsg).unwrap()
