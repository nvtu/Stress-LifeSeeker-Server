from constants.security_settings import SECRET_KEY, TOKEN_HASH_ALGORITHM, PASSWORD_HASH_ALGORITHM
from fastapi import APIRouter, Depends, status, HTTPException
from schemas.security_schemas import Token
from internal.security.authenticator import Authenticator
from internal.security.token_generator import TokenGenerator
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from constants.token_configuration import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix = '/auth',
    tags = ['auth'],
    responses = {
        401: {
            "description": "Unauthorized Request"
        }
    }
)


authenticator = Authenticator(PASSWORD_HASH_ALGORITHM)
token_generator = TokenGenerator(SECRET_KEY, TOKEN_HASH_ALGORITHM)


@router.post('', response_model = Token)
async def authenticate_user_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticator.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    tokens = token_generator.create_authentication_token(
        data={"username": form_data.username}, 
        expires_delta=access_token_expires
    )
    return tokens


