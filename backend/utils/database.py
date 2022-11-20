from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config
from urllib import parse


DATABASE_CONFIG = Config.MariaDB
DATABASE_URL = f'mysql://{DATABASE_CONFIG["user"]}:{parse.quote(DATABASE_CONFIG["password"])}@{DATABASE_CONFIG["host"]}/{DATABASE_CONFIG["database"]}'

engine = create_engine(DATABASE_URL)


def get_db():
    databaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        yield databaseSession()
    except Exception as e:
        print(f"database error {e}")

    finally:
        try:
            databaseSession.close_all()
        except Exception as e:
            pass
