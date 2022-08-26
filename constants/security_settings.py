import os

secret_path = os.path.abspath('secret.txt')
data = [line.rstrip() for line in open(secret_path).readlines()]
SECRET_KEY, TOKEN_HASH_ALGORITHM, PASSWORD_HASH_ALGORITHM = data