from option import *
from pydantic import *

# create tag
class Tag_create(BaseModel):
    name: str = ""
    slug: str = ""
    color: str = ""
