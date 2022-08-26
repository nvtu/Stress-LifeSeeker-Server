from shutil import ExecError
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sql_app.dependencies import get_sqldb_session
from sqlalchemy.orm import Session
from sql_app.schemas import *
from sql_app import crud
from schemas.security_schemas import (
    User as UserSchema,
)
from typing import List
from schemas.request_schemas import RequestUserCreate
from dependencies import verify_token
from internal.transfer.upload import handle_upload_file, save_file_internally


router = APIRouter(
    prefix = '/users',
    tags = ['users'],
)


@router.post("/create_user", response_model = UserSchema)
def create_user(user: RequestUserCreate, db: Session = Depends(get_sqldb_session)):
    db_user = crud.get_user(db, username = user.username)
    if db_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="User already registered")
    return crud.create_user(db=db, user=user)


@router.get("/get_user/{username}", response_model = UserSchema)
def get_user(username: str, db: Session = Depends(get_sqldb_session)):
    db_user = crud.get_user(db, username = username)
    if db_user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.get("/get_user_list", response_model= List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_sqldb_session)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/upload_file", status_code = status.HTTP_202_ACCEPTED)
async def upload_file(file: UploadFile, user_id: str = Depends(verify_token)):
    try:
        handle_upload_file(file, save_file_internally)
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Upload error ---!!!!")
    return {"message": "File uploaded successfully"}