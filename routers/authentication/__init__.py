import os


secret_path = os.path.abspath('secret.txt')
SECRET_KEY = open(secret_path).read().strip()
