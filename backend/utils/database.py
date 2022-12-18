from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config
from urllib import parse
import random


DATABASE_CONFIG = Config.MariaDB
DATABASE_URL = f'mysql+pymysql://{DATABASE_CONFIG["user"]}:{parse.quote(DATABASE_CONFIG["password"])}@{DATABASE_CONFIG["host"]}/{DATABASE_CONFIG["database"]}'

engine = create_engine(
    DATABASE_URL, connect_args={"connect_timeout": 3}, pool_size=100, max_overflow=10
)
databaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    # rand_token = random.randint(0, 100000)
    db_session = databaseSession()
    try:
        yield db_session
    except:
        try:
            db_session.rollback()
        except:
            pass
    finally:
        db_session.close()
