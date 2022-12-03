from pydantic import *
from typing import Optional


class run_request(BaseModel):
    language: str
    code: str


class run_input(BaseModel):
    input: str
