from option import *

from config import Config
from fastapi import FastAPI
import user

app = FastAPI(title="kuku-api")
app.include_router(user.router)


@app.get("/")
async def main():
    return {"message": "Helloworld FastAPI", "data": user.schemas.Test()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=Config.HTTP["port"], reload=True)
