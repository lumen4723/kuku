from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from .schemas import board_free_create
from utils.session import *
from board.free.like.database import *

router = APIRouter(
    prefix="/board/free",
    tags=["board_free"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def user(session: Session = Depends(utils.database.get_db)):
    return database.list_article(session, all=True).map_err(throwMsg).unwrap()


# create article router
@router.post(
    "/create", dependencies=[Depends(cookie)], status_code=status.HTTP_201_CREATED
)
async def create_article(
    article: board_free_create,
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
@router.get("/article_id/{article_id}")
async def get_article_by_id(
    article_id: int, session: Session = Depends(utils.database.get_db)
):
    return database.get_article_by_id(article_id, session).map_err(throwMsg).unwrap()


# get article by uid router
@router.get("/uid/{uid}")
async def get_article_by_uid(
    uid: int, session: Session = Depends(utils.database.get_db)
):
    return database.get_article_by_uid(uid, session).map_err(throwMsg).unwrap()


# delete articles from database
@router.delete("/delete/{article_id}", dependencies=[Depends(cookie)])
async def delete_article(
    article_id: int,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        database.delete_article(article_id, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


# update article
@router.put("/update/{article_id}", dependencies=[Depends(cookie)])
async def update_article(
    article_id: int,
    article: board_free_create,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        database.update_article(article_id, session_data.uid, article, session)
        .map_err(throwMsg)
        .unwrap()
    )


# like article by id router
@router.post(
    "/article/{article_id}/like",
    dependencies=[Depends(cookie)],
    status_code=status.HTTP_201_CREATED,
)
async def like_article_by_id(
    article_id: int,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        create_free_like(article_id, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


@router.put(
    "/article/{article_id}/dislike",
    dependencies=[Depends(cookie)],
    status_code=status.HTTP_201_CREATED,
)
async def dislike_article_by_id(
    article_id: int,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        cancel_free_like(article_id, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


# get article start ~ end page router
@router.get("/list/like/get/{start_page}")
async def list_article(
    start_page: int, limit: int = 20, session: Session = Depends(utils.database.get_db)
):
    return (
        database.list_article(session, page=start_page, limit=limit, like=True)
        .map_err(throwMsg)
        .unwrap()
    )


@router.get("/list/like/getall")
async def user(session: Session = Depends(utils.database.get_db)):
    return (
        database.list_article(session, all=True, like=True).map_err(throwMsg).unwrap()
    )
