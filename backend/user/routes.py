from . import database, schemas
from fastapi import APIRouter, Depends
from option import *
import utils

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def user(email: str, db=Depends(utils.database.get_db)):
    return database.get_user_by_email(email, db)
