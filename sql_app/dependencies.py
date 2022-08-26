from connectors import sqlalchemy_session


def get_sqldb_session():
    db = sqlalchemy_session()
    try:
        yield db
    finally:
        db.close()