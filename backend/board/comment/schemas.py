from option import *
from pydantic import *


class board_free_comment_create(BaseModel):
    content: str = ''