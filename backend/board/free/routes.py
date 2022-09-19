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


@router.get("/")
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

# # user 계성 생성 라우터 함수
# @router.post("/user", status_code=status.HTTP_201_CREATED)
# async def create_user(
#     user: createuser, session: Session = Depends(utils.database.get_db)
# ):
#     return database.create_user(user, session).map_err(
#         throwMsg
#     )


# # 모든 user 정보 보여주는 함수
# @router.get("/all")
# async def all_user(session: Session = Depends(utils.database.get_db)):
#     return session.query(database.User).all()
