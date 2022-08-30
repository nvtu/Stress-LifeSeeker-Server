from fastapi import HTTPException, status, Header
from constants.security_settings import SECRET_KEY, TOKEN_HASH_ALGORITHM, PASSWORD_HASH_ALGORITHM
from internal.security.token_decoder import TokenDecoder
from internal.security.authenticator import Authenticator
from jose import JWTError


token_decoder = TokenDecoder(SECRET_KEY, TOKEN_HASH_ALGORITHM)
authenticator = Authenticator(PASSWORD_HASH_ALGORITHM)
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

expired_creditentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)


async def verify_token(token: str = Header(...)):
    try:
        payload = token_decoder.decode(token)
        username = payload.get("username") # Check if the username is in the payload
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if not authenticator.verify_user(username): # Check if the user is actually in the database
        raise credentials_exception
    if not authenticator.verify_user_time_info(username, payload.get("iat")):
        raise credentials_exception
    if not authenticator.verify_expiration_time(payload.get("exp")):
        raise expired_creditentials_exception
    return username





