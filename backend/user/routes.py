from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from .schemas import createuser, loginuser
from utils.exception import throwMsg
from fastapi import Response, Depends
from uuid import UUID, uuid4
from utils.session import *

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
    return database.create_user(user, session).map_err(throwMsg).unwrap()


# 모든 user 정보 보여주는 함수
@router.get("/all")
async def all_user(session: Session = Depends(utils.database.get_db)):
    return session.query(database.User).all()


@router.post("/login")
async def create_session(
    user: loginuser,
    response: Response,
    session: Session = Depends(utils.database.get_db),
):
    uid = database.login(user, session).map_err(throwMsg).unwrap()
    uuidSession = uuid4()
    data = SessionData(uid=uid)

    await backend.create(uuidSession, data)
    cookie.attach_to_response(response, uuidSession)

    return database.get_user_by_uid(uid, session).map_err(throwMsg).unwrap()


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(
    session_data: SessionData = Depends(verifier),
    session: Session = Depends(utils.database.get_db),
):
    return (
        database.get_user_by_uid(session_data.uid, session).map_err(throwMsg).unwrap()
    )


@router.post("/logout")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"
