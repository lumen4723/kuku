from . import database, schema
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from utils.session import *

router = APIRouter(
    prefix="/run",
    tags=["run"],
    responses={404: {"description": "Not found"}},
)

run_submit_user = {}


@router.post("/", dependencies=[])
async def main(
    form: schema.run_request,
    db: Session = Depends(utils.database.get_db),
    session_id=Depends(cookie)
    # session_data: SessionData = Depends(verifier),
):
    # if session_data.type != 0:
    # return throwMsg("권한이 없습니다.")

    form = database.code_jobs(**form.dict(), status="que")
    run_id = database.create_run_requst(form, db).map_err(throwMsg).unwrap()

    run_submit_user[run_id] = session_id
    return run_id


@router.get("/{run_id}/", dependencies=[Depends(cookie)])
async def get_run(
    run_id: int,
    db: Session = Depends(utils.database.get_db),
    session_id=Depends(cookie),
):
    if run_id not in run_submit_user:
        return throwMsg("종료된 요청")

    if run_submit_user[run_id] != session_id:
        return throwMsg("권한이 없습니다.")

    result = database.get_run_requst(run_id, db).map_err(throwMsg).unwrap()
    if result.status != "que" and result.last_read_line is None:
        result.last_read_line = 0

    output = result.output
    if result.output != None:
        output = result.output.split("\n")
        read_cursor = len(output)

        print(output)
        output = tuple(
            filter(
                lambda s: s.startswith("===") == False, output[result.last_read_line :]
            )
        )
        print(output)

        database.update_run_request_last_read_line(run_id, read_cursor, db)

    return {
        "status": result.status,
        "status_updated": result.status_updated,
        "output": output,
        "last_read_line": result.last_read_line,
    }


@router.put("/{run_id}/input", dependencies=[Depends(cookie)])
async def pass_input_to_program(
    run_id: int,
    db: Session = Depends(utils.database.get_db),
    session_id=Depends(cookie),
):
    if run_submit_user[run_id] != session_id:
        return throwMsg("권한이 없습니다.")
