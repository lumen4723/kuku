from datetime import datetime
from mimetypes import init
from option import *
from pydantic import *


class User(BaseModel):
    username: str = ""
    password: str = ""


# create_user class
class createuser(BaseModel):
    username: str = ""
    password: str = ""
    email: str = ""


# longin user class methods
class loginuser(BaseModel):
    email: str = ""
    password: str = ""


class UserInformation(BaseModel):
    userid: int = 0
    username: str = ""
    email: str = ""
    created: datetime