from option import *
from pydantic import *

# create board_free aritcle schemas
class board_qna_create(BaseModel):
    title: str = ''
    content: str = ''