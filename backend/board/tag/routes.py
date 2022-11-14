from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from utils.session import *
from .schemas import Tag_create

router = APIRouter(
    prefix="/board/tag",
    tags=["tag"],
    responses={404: {"description": "Not found"}},
)

# get all tag
@router.get("/list")
async def list_tag(session: Session = Depends(utils.database.get_db)):
    return database.get_all_tags(session).map_err(throwMsg).unwrap()


# create a new tag
@router.post(
    "/create", dependencies=[Depends(cookie)], status_code=status.HTTP_201_CREATED
)
async def create_tag(
    tag: Tag_create, session: Session = Depends(utils.database.get_db)
):
    return database.create_tag(tag, session).map_err(throwMsg).unwrap()


# get id by slug
@router.get("/get_id_by_slug/{slug}")
async def get_id_by_slug(slug: str, session: Session = Depends(utils.database.get_db)):
    return database.get_id_by_slug(slug, session).map_err(throwMsg).unwrap()

@router.get("/get_name_by_slug/{slug}")
async def get_name_by_slug(slug: str, session: Session = Depends(utils.database.get_db)):
    return database.get_name_by_slug(slug, session).map_err(throwMsg).unwrap()
