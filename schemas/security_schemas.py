from faulthandler import disable
from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    disabled: Union[bool, None] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "nvtu",
                "email": "nvtu@gmail.com",
                "disabled": False,
            }
        }


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class Payload(BaseModel):
    username: str
    exp: int
    iat: int
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "username": "nvtu",
                "exp": 1598451820,
                "iat": 1598451820,
                "token_type": "access",
            }
        }
