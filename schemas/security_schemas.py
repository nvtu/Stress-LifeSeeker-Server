from faulthandler import disable
from pydantic import BaseModel
from typing import Union


class UserBase(BaseModel):
    username: str

    class Config:
        scheme_extra = {
            "example": {
                "username": "nvtu",
            }
        }


class User(UserBase):
    name: str 

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "nvtu",
                "name": "Van-Tu Ninh"
            }
        }


class UserInDB(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "nvtu",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
            }
        }


class ExpirationTime(UserBase):
    exp: int
    iat: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "nvtu",
                "exp": 1598446800,
                "iat": 1598446800
            }
        }



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
