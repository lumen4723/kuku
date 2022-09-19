from option import *
from pydantic import *

class User(BaseModel):
    username: str = ''
    password: str = ''

    # def __init__(self, username: str, password: str):
    #     self.username = username
    #     self.password = password

#create_user class
class createuser(BaseModel):
    username: str = ''
    password: str = ''
    email: str = ''

    # def __init__(self, username: str, password: str, email: str):
    #     self.username = username
    #     self.password = password
    #     self.email = email