from passlib.context import CryptContext


class HashGenerator:

    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


    def hash_string(self, string: str) -> str:
        return self.pwd_context.hash(string)