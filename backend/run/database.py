from option import *
from sqlalchemy.orm import Session, joinedload
import sqlalchemy
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from utils.exception import *
from datetime import datetime


class code_jobs(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    language: str
    code: str

    status: str
    error: Optional[str]
    status_updated: datetime = Field(default=datetime.now())

    output: Optional[str]
    last_read_line: Optional[int]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.language = kwargs.get("language", None)
        self.code = kwargs.get("code", None)
        self.status = kwargs.get("status", None)
        self.status_updated = kwargs.get("status_updated", None)
        self.output = kwargs.get("output", None)
        self.last_read_line = kwargs.get("last_read_line", None)
        self.error = kwargs.get("error", None)


class code_control(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int
    ctrl: str
    data: str
    status: str = Field(default=0)

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.job_id = kwargs.get("job_id", None)
        self.status = kwargs.get("status", None)
        self.ctrl = kwargs.get("ctrl", None)
        self.data = kwargs.get("data", None)


def create_run_requst(form: code_jobs, db: Session) -> Result[int, str]:
    try:
        db.add(form)
        db.commit()
        db.refresh(form)
        return Ok(form.id)
    except Exception as e:
        return Err(str(e))


def create_input_request(job_id: int, input: str, db: Session) -> Result[int, str]:
    try:
        db.add(code_control(job_id=job_id, ctrl="input", data=input))
        db.commit()
        return Ok(1)
    except Exception as e:
        return Err(str(e))


def get_run_requst(run_id: int, db: Session) -> Result[code_jobs, str]:
    try:
        run = (
            db.query(
                code_jobs.status,
                code_jobs.status_updated,
                code_jobs.output,
                code_jobs.error,
            )
            .filter(code_jobs.id == run_id)
            .first()
        )

        return Ok(code_jobs(**run))
    except Exception as e:
        return Err(str(e))


def update_run_request_last_read_line(
    run_id: int, last_read_line: int, db: Session
) -> Result[code_jobs, str]:
    try:
        run = db.query(code_jobs).filter(code_jobs.id == run_id).first()
        run.last_read_line = last_read_line
        db.add(run)
        db.commit()
        return Ok(run)
    except Exception as e:
        print(e)
        return Err(str(e))
