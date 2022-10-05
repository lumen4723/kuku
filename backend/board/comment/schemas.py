from option import *
from pydantic import *


class board_comment_create(BaseModel):
    content: str = ''