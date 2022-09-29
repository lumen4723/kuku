from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from .schemas import board_qna_create
from utils.session import *

router = APIRouter(
    prefix="/board/qna",
    tags=["board_qna"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def user(session: Session = Depends(utils.database.get_db)):
    return database.list_article(session, all=True).map_err(throwMsg).unwrap()


# create article router
@router.post(
    "/article", dependencies=[Depends(cookie)], status_code=status.HTTP_201_CREATED
)
async def create_article(
    article: board_qna_create,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        database.create_article(article, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


# get article start ~ end page router
@router.get("/list/{start_page}")
async def list_article(
    start_page: int, limit: int = 20, session: Session = Depends(utils.database.get_db)
):
    return (
        database.list_article(session, page=start_page, limit=limit)
        .map_err(throwMsg)
        .unwrap()
    )


# get article by id router
@router.get("/article/{article_id}")
async def get_article_by_id(
    article_id: int, session: Session = Depends(utils.database.get_db)
):
    return database.get_article(article_id, session).map_err(throwMsg).unwrap()
