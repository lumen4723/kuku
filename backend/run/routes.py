from . import database, schema
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from utils.session import *
import re

router = APIRouter(
    prefix="/run",
    tags=["run"],
    responses={404: {"description": "Not found"}},
)

run_submit_user = {}


@router.post("/")
def main(
    form: schema.run_request,
    db: Session = Depends(utils.database.get_db),
    # session_id=Depends(cookie)
    # session_data: SessionData = Depends(verifier),
):
    # if session_data.type != 0:
    # return throwMsg("권한이 없습니다.")

    form = database.code_jobs(**form.dict(), status="que")
    run_id = database.create_run_requst(form, db).map_err(throwMsg).unwrap()

    # run_submit_user[run_id] = session_id
    return run_id


@router.get("/{run_id}/")
def get_run(
    run_id: int,
    db: Session = Depends(utils.database.get_db),
    # session_id=Depends(cookie),
):
    result = database.get_run_requst(run_id, db).map_err(throwMsg).unwrap()

    output = result.output
    if result.output != None:
        output = result.output.split("\n")

        for i in range(len(output)):
            if output[i].startswith("=== kuku =============") is False:
                continue

            compiler_exit_code_match = re.search(
                "=== kuku ============= (\d+) ===============", output[i]
            )
            if compiler_exit_code_match is None:
                continue

            exit_code = compiler_exit_code_match.group(1)
            if exit_code != "0":
                output[i] = "컴파일러 오류: " + exit_code

        output = tuple(
            filter(
                lambda x: x.startswith("=== kuku ===") is False,
                output[result.last_read_line :],
            )
        )

        output = tuple(map(lambda v: {"id": v[0], "data": v[1]}, enumerate(output)))

    return {
        "status": result.status,
        "status_updated": result.status_updated,
        "output": output,
        "error": result.error,
    }


@router.put("/{run_id}/input", dependencies=[])
def pass_input_to_program(
    form: schema.run_input,
    run_id: int,
    db: Session = Depends(utils.database.get_db),
):
    database.create_input_request(run_id, form.input, db).map_err(throwMsg).unwrap()
    return {"status": "ok"}
