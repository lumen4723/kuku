from option import *

from config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import user
import board.free
import board.qna
import board.tag
import study
import upload
import run

app = FastAPI(title="kuku-api")
app.include_router(user.router)
app.include_router(board.free.router)
app.include_router(board.qna.router)
app.include_router(board.tag.router)
app.include_router(study.router)
app.include_router(upload.router)
app.include_router(run.router)

origins = ["https://eyo.kr", "https://www.eyo.kr"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello!! fastapi"}


if __name__ == "__main__":
    import uvicorn

    print("port -> ", Config.HTTP["port"])
    uvicorn.run("main:app", host="0.0.0.0", port=Config.HTTP["port"], reload=True)
