from option import *
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel
from typing import Optional
from utils.exception import *


class board_information(SQLModel, table=True):
    information_id: Optional[int] = Field(default=None, primary_key=True)
    size: Optional[int] = Field(default=0)
    description: str = Field(sa_column_kwargs={"name": "description", "unique": True})


# create board information if type is 0 add size else sub size
def add_tag(description: str, type: int, db: Session) -> Result:
    try:
        get_board = (
            db.query(board_information)
            .filter(board_information.description == description)
            .first()
        )
        if get_board is None:
            board = board_information(description=description)
            db.add(board)
            db.commit()
            db.refresh(board)
            return Ok(board)
        elif type == 0:
            get_board.size += 1
        elif get_board.size > 0:
            get_board.size -= 1
        else:
            return Err("form data is not valid")
        db.add(get_board)
        db.commit()
        db.refresh(get_board)
        return Ok(get_board)
    except Exception as e:
        return Err(DefaultException("unknown error"))
