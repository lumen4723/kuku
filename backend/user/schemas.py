from option import *


class User:
    username: str = NONE
    password: Option[str] = NONE

    def __init__(self, username: str, password: Option[str]):
        self.username = username
        self.password = password
