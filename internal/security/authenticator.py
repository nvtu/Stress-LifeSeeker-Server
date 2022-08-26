from passlib.context import CryptContext
from schemas.security_schemas import UserInDB
from sql_app.dependencies import sqlalchemy_session
from sqlalchemy.orm import Session
from sql_app import crud
from datetime import datetime
import sentry_sdk


class Authenticator:

    def __init__(self, algorithm: str):
        self.pwd_context = CryptContext(schemes=[algorithm], deprecated='auto')


    def authenticate(self, username: str, password: str) -> bool:
        user = self.__get_user(username)
        print(user)
        if not user or not self.__verify_password(password, user.hashed_password):
            return False
        return True


    def verify_user(self, username: str, db: Session = sqlalchemy_session()) -> bool:
        """
        Check if the user is actually in the database
        """
        try:
            user = crud.get_user(db, username=username) 
            db.close()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            db.close()
            return False
        return user is not None

    
    def verify_user_time_info(self, username: str, iat: int, db: Session = sqlalchemy_session()) -> bool:
        """
        Check if the issue time of the token is valid
        """
        try:
            user = crud.get_user_expiration_time(db, username = username)
            db.close()
            return user.iat == iat
        except Exception as e:
            sentry_sdk.capture_exception(e)
            db.close()
            return False


    def verify_expiration_time(self, exp: int):
        """"
        Check if the expiration time of the token is valid
        """
        return exp > datetime.utcnow().timestamp()


    def __get_user(self, username: str, db: Session = sqlalchemy_session()):
        try:
            user = crud.get_user_in_db(db, username=username)
            db.close()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            db.close()
        return user


    def __verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)