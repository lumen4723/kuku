from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from .schemas import board_free_create
router = APIRouter(
    prefix="/board_free",
    tags=["board_free"],
    responses={404: {"description": "Not found"}},
)


@router.get("/getAll")
async def user( session: Session = Depends(utils.database.get_db)):
    return database.get_all_article_free(session)

#create article router
@router.post("/article", status_code=status.HTTP_201_CREATED)
async def create_article(
    article: board_free_create, session: Session = Depends(utils.database.get_db)
):
    return database.create_article(article, session).map_err(
        throwMsg
    ).unwrap()

# get article start ~ end page router
@router.get("/get")
async def get_article(
    start_page: int, session: Session = Depends(utils.database.get_db)
):
    return database.get_article(start_page, session).map_err(throwMsg).unwrap()
