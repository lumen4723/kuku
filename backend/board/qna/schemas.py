from typing import List
from option import *
from pydantic import *
# create board_free aritcle schemas
class Board_qna_question(BaseModel):
    title: str = ''
    content: str = ''
    tags: List[str] = []

class Board_qna_answer(BaseModel):
    title: str = ''
    content: str = ''
    parentid: int = 0