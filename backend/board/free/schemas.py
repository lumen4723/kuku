from option import *
from pydantic import *

# create board_free aritcle schemas
class board_free_create(BaseModel):
    title: str = ""
    content: str = ""


class board_free_comment_create(BaseModel):
    content: str = ""
