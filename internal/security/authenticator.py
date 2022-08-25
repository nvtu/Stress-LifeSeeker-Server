from passlib.context import CryptContext
from schemas.security_schemas import UserInDB


db = {
    "nvtu": {
        "username": "nvtu",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class Authenticator:

    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


    def authenticate(self, username: str, password: str) -> bool:
        user = self.__get_user(username)
        if not user or not self.__verify_password(password, user.hashed_password):
            return False
        return True


    def verify_user(self, username: str) -> bool:
        """
        Check if the user is actually in the database
        """
        return username in db


    def __get_user(self, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)


    def __verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)