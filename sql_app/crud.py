from sqlalchemy.orm import Session
from internal.security.hash_generator import HashGenerator
from schemas.request_schemas import RequestUserCreate

from .schemas import (
    User as ORMUser,
    UserInDB as ORMUserInDB,
    ExpirationTime as ORMExpirationTime,
)


def get_user(db: Session, username: str):
    return db.query(ORMUser).filter(ORMUser.username == username).first()


def get_user_in_db(db: Session, username: str):
    return db.query(ORMUserInDB).filter(ORMUserInDB.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ORMUser).offset(skip).limit(limit).all()


def get_user_expiration_time(db: Session, username: str):
    return db.query(ORMExpirationTime).filter(ORMExpirationTime.username == username).first()


def create_user(db: Session, user: RequestUserCreate):
    hash_machine = HashGenerator()
    hashed_password = hash_machine.hash_string(user.password)

    # Add user's secret data to database
    db_user = ORMUserInDB(username = user.username, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Add user's public data to database
    db_user = ORMUser(username = user.username, name = user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_user_in_expiration_time(db: Session, username: str , exp: int, iat: int):
    db_user = ORMExpirationTime(username = username, exp = exp, iat = iat)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user_expiration_time_info(db: Session, username: str, exp: int, iat: int):
    db_user = db.query(ORMExpirationTime).get(username)
    print(db_user)
    db_user.exp = exp
    db_user.iat = iat
    db.commit()
    db.refresh(db_user)

    return db_user
