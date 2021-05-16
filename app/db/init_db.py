from app.db.session import engine
from app.db.session import db_session as session

from app.db import models
from app.db.base import Base


def init_db(db_session):
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db(session)
