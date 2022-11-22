from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config
from urllib import parse


DATABASE_CONFIG = Config.MariaDB
DATABASE_URL = f'mysql://{DATABASE_CONFIG["user"]}:{parse.quote(DATABASE_CONFIG["password"])}@{DATABASE_CONFIG["host"]}/{DATABASE_CONFIG["database"]}'

engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 3})


def get_db():
    databaseSession = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    try:
        yield databaseSession()
    except:
        databaseSession.rollback()
        raise
    finally:
        databaseSession.remove()
