import os


secret_path = os.path.abspath('secret.txt')
data = [line.rstrip() for line in open(secret_path).readlines()]
SECRET_KEY, HASH_ALGORITHM = data