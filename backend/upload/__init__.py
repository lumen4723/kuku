# ckeditor image simple upload

import random
import string
import utils
from fastapi import APIRouter, Depends, status
from option import *
from utils.exception import throwMsg
from utils.session import *
from board.free.like.database import *
from board.free.comment.database import *
from fastapi import FastAPI, File, UploadFile
import os

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def upload_image(upload: UploadFile):
    contents = await upload.read()

    extension = upload.filename.split(".")[-1].lower()
    if extension not in ["jpg", "gif", "png", "jpeg"]:
        raise Exception("invaild extension")

    filename = (
        "".join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            )
            for _ in range(32)
        )
        + "."
        + extension
    )

    with open(os.path.join("/kuku/upload/", filename), "wb") as fp:
        fp.write(contents)

    return {"url": "https://eyo.kr:8081/upload/files/" + filename}
