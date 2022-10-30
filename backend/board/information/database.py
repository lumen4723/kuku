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
def change_information(
    description: str, increase: bool, db: Session, commit: bool = True
) -> Result[None, str]:
    try:
        is_update_succss = (
            db.query(board_information)
            .filter(board_information.description == description)
            .update(
                {
                    "size": board_information.size + 1
                    if increase
                    else board_information.size - 1
                }
            )
            > 0
        )

        if is_update_succss is False:
            db.add(
                board_information(description=description, size=1 if increase else 0)
            )

        if commit:
            db.commit()

        return Ok(True)
    except Exception as e:
        return Err("change information error")
