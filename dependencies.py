from fastapi import HTTPException, status, Header
from routers.authentication.__init__ import SECRET_KEY
from internal.security.token_decoder import TokenDecoder
from internal.security.authenticator import Authenticator
from jose import JWTError


token_decoder = TokenDecoder(SECRET_KEY)
authenticator = Authenticator()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def verify_token(token: str = Header(...)):
    try:
        payload = token_decoder.decode(token)
        username = payload.get("sub") # Check if the username is in the payload
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if not authenticator.verify_user(payload["sub"]): # Check if the user is actually in the database
        raise credentials_exception
    return username
