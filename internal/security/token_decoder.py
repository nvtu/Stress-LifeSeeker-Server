from jose import jwt, JWTError
from fastapi import HTTPException, status
from schemas.security_schemas import Payload


class TokenDecoder:

    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm


    def decode(self, token: str):
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        return payload