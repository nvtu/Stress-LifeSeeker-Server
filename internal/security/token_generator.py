from typing import Union
from datetime import timedelta, datetime
from schemas.security_schemas import Token
from jose import jwt


class TokenGenerator:

    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        self.algorithm = algorithm
        self.secret_key = secret_key


    def __create_token(self, data: dict):
        encoded_jwt = jwt.encode(data.copy(), self.secret_key, algorithm=self.algorithm)
        return encoded_jwt


    def create_authentication_token(self, data: dict, expires_delta: Union[timedelta, None] = None) -> Token:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes = 15)
        to_encode.update({
            "exp": expire, 
            "iat": datetime.utcnow(), 
        })

        tokens = Token(
            access_token = self.__create_access_token(to_encode),
            refresh_token = self.__create_refresh_token(to_encode),
        )

        return tokens


    def __create_access_token(self, data: dict):
        to_encode = data.copy()
        to_encode.update({'token_type': 'access'})
        return self.__create_token(to_encode)


    def __create_refresh_token(self, data: dict):
        to_encode = data.copy()
        to_encode.update({'token_type': 'refresh'})
        return self.__create_token(to_encode)
 