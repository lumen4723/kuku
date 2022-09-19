from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from .schemas import createuser
from utils.exception import throwMsg

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def user(email: str, session: Session = Depends(utils.database.get_db)):
    return database.get_user_by_email(email, session)


# user 계성 생성 라우터 함수
@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: createuser, session: Session = Depends(utils.database.get_db)
):
    return database.create_user(user, session).map_err(
        throwMsg
    ).unwrap()


# 모든 user 정보 보여주는 함수
@router.get("/all")
async def all_user(session: Session = Depends(utils.database.get_db)):
    return session.query(database.User).all()
