from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from .schemas import Board_qna_question, Board_qna_answer
from utils.session import *
from board.qna.like.database import cancel_qna_like, create_qna_like

router = APIRouter(
    prefix="/board/qna",
    tags=["board_qna"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
def list(session: Session = Depends(utils.database.get_db)):
    return database.list_article(session, all=True).map_err(throwMsg).unwrap()


# get article start ~ end page router
@router.get("/list/{start_page}")
def list_article(
    start_page: int, limit: int = 20, session: Session = Depends(utils.database.get_db)
):
    return (
        database.list_article(session, page=start_page, limit=limit)
        .map_err(throwMsg)
        .unwrap()
    )


# create article router
@router.post(
    "/question", dependencies=[Depends(cookie)], status_code=status.HTTP_201_CREATED
)
def create_question(
    article: Board_qna_question,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        database.create_question(article, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


# get article question router
@router.get("/list/answer/{parent_id}")
def get_answer(
    parent_id: int,
    session: Session = Depends(utils.database.get_db),
):
    return database.list_article(session, aid=parent_id).map_err(throwMsg).unwrap()


# create article router
@router.post(
    "/answer", dependencies=[Depends(cookie)], status_code=status.HTTP_201_CREATED
)
def create_answer(
    article: Board_qna_answer,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        database.create_answer(article, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


# get article by slug
@router.get("/list/slug/{slug}")
def list_article_with_slug(
    slug: str, session: Session = Depends(utils.database.get_db)
):
    return (
        database.list_article_by_slug(session, slug=slug, all=True)
        .map_err(throwMsg)
        .unwrap()
    )


# get article by slug start_page
@router.get("/list/slug/{slug}/{start_page}")
def list_article_with_slug_and_page(
    slug: str,
    start_page: int,
    limit: int = 20,
    session: Session = Depends(utils.database.get_db),
):
    return (
        database.list_article_by_slug(session, slug=slug, page=start_page, limit=limit)
        .map_err(throwMsg)
        .unwrap()
    )


# get article by id router
@router.get("/list/article/{article_id}")
def get_article_by_id(
    article_id: int, session: Session = Depends(utils.database.get_db)
):
    return database.get_article(article_id, session).map_err(throwMsg).unwrap()


# delete article by id router
@router.delete(
    "/delete/{article_id}",
    dependencies=[Depends(cookie)],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_article_by_id(
    article_id: int,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return {
        "isOk": database.delete_article(article_id, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    }


# update article by id router
@router.put(
    "/article/{article_id}",
    dependencies=[Depends(cookie)],
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_article_by_id(
    article_id: int,
    article: Board_qna_question,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        database.update_article(article, article_id, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


# update answer by id router
@router.put(
    "/answer/{answer_id}",
    dependencies=[Depends(cookie)],
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_answer_by_id(
    answer_id: int,
    answer: Board_qna_answer,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        database.update_answer(answer, answer_id, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


# like article by id router
@router.post(
    "/article/{article_id}/like",
    dependencies=[Depends(cookie)],
    status_code=status.HTTP_201_CREATED,
)
def like_article_by_id(
    article_id: int,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return {
        "isOk": create_qna_like(article_id, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    }


@router.put(
    "/article/{article_id}/dislike",
    dependencies=[Depends(cookie)],
    status_code=status.HTTP_201_CREATED,
)
def dislike_article_by_id(
    article_id: int,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    return (
        cancel_qna_like(article_id, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


# @router.get("/list/like/get/{start_page}")
# def list_article_with_get(
#     start_page: int, limit: int = 20, session: Session = Depends(utils.database.get_db)
# ):
#     return (
#         database.list_article(session, page=start_page, limit=limit, like=True)
#         .map_err(throwMsg)
#         .unwrap()
#     )


# @router.get("/list/slug/like/getall/{slug}")
# def get_article(slug: str, session: Session = Depends(utils.database.get_db)):
#     return (
#         database.list_article_by_slug(session, slug=slug, all=True, like=True)
#         .map_err(throwMsg)
#         .unwrap()
#     )


# @router.get("/list/slug/like/get/{slug}/{start_page}")
# def get_article(
#     slug: str,
#     start_page: int,
#     limit: int = 20,
#     session: Session = Depends(utils.database.get_db),
# ):
#     return (
#         database.list_article_by_slug(
#             session, slug=slug, page=start_page, limit=limit, like=True
#         )
#         .map_err(throwMsg)
#         .unwrap()
#     )


# get article by title
@router.get("/search/title/{title}")
def search_article_by_title(
    title: str,
    page: int,
    limit: int = 20,
    session: Session = Depends(utils.database.get_db),
):
    return (
        database.get_article_by_title(title, session, page, limit)
        .map_err(throwMsg)
        .unwrap()
    )


# get article by username
@router.get("/search/username/{username}")
def search_article_by_username(
    username: str,
    page: int,
    limit: int = 20,
    session: Session = Depends(utils.database.get_db),
):
    return (
        database.get_article_by_username(username, session, page, limit)
        .map_err(throwMsg)
        .unwrap()
    )


# get article by content
@router.get("/search/content/{content}")
def search_article_by_content(
    content: str,
    page: int,
    limit: int = 20,
    session: Session = Depends(utils.database.get_db),
):
    return (
        database.get_article_by_content(content, session, page, limit)
        .map_err(throwMsg)
        .unwrap()
    )
