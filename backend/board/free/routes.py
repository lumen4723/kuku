from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from .schemas import board_free_create
from utils.session import *
router = APIRouter(
    prefix="/board_free",
    tags=["board_free"],
    responses={404: {"description": "Not found"}},
)


@router.get("/getAll")
async def user( session: Session = Depends(utils.database.get_db)):
    return database.get_all_article_free(session)

#create article router
@router.post("/article", dependencies=[Depends(cookie)],status_code=status.HTTP_201_CREATED)
async def create_article(
    article: board_free_create, session: Session = Depends(utils.database.get_db), session_data: SessionData = Depends(verifier)
):
    return database.create_article(article,session_data.uid, session).map_err(
        throwMsg
    ).unwrap()

# get article start ~ end page router
@router.get("/getByPage")
async def get_article(
    start_page: int, session: Session = Depends(utils.database.get_db)
):
    return database.get_article(start_page, session).map_err(throwMsg).unwrap()

#get article by id router
@router.get("/getById")
async def get_article_by_id(
    id: int, session: Session = Depends(utils.database.get_db)
):
    return database.get_article_by_id(id, session).map_err(throwMsg).unwrap()
    