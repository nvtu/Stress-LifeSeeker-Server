from typing import Union
from datetime import timedelta, datetime
from schemas.security_schemas import Token
from sql_app.dependencies import sqlalchemy_session
from sqlalchemy.orm import Session
from sql_app import crud
from jose import jwt


class TokenGenerator:

    def __init__(self, secret_key: str, algorithm: str):
        self.algorithm = algorithm
        self.secret_key = secret_key


    def __create_token(self, data: dict):
        encoded_jwt = jwt.encode(data.copy(), self.secret_key, algorithm=self.algorithm)
        return encoded_jwt


    def create_authentication_token(self, data: dict, expires_delta: Union[timedelta, None] = None) -> Token:
        to_encode = data.copy()
        iat = datetime.utcnow()
        if expires_delta:
            expire = iat + expires_delta
        else:
            expire = iat + timedelta(minutes = 15)

        to_encode.update({
            "exp": int(expire.timestamp()), 
            "iat": int(iat.timestamp()),
        })

        self.__insert_token_payload_to_db(to_encode)
        
        tokens = Token(
            access_token = self.__create_access_token(to_encode),
            refresh_token = self.__create_refresh_token(to_encode),
        )

        return tokens

    
    def __insert_token_payload_to_db(self, data: dict, db: Session = sqlalchemy_session()):
        try:
            if not crud.get_user_expiration_time(db, data["username"]):
                crud.create_user_in_expiration_time(db, **data)
            else:
                crud.update_user_expiration_time_info(db, **data)
            db.close()
        except Exception as e:
            db.close()


    def __create_access_token(self, data: dict):
        to_encode = data.copy()
        to_encode.update({'token_type': 'access'})
        return self.__create_token(to_encode)


    def __create_refresh_token(self, data: dict):
        to_encode = data.copy()
        to_encode.update({'token_type': 'refresh'})
        return self.__create_token(to_encode)
 