from fastapi import APIRouter, status, HTTPException, Depends

from fastapi.encoders import jsonable_encoder
from schemas.db_schemas import UserModel
from schemas.response_schemas import ResponseListDates
from schemas.request_schemas import RequestModifyListDates
import sentry_sdk
import connectors
from dependencies import verify_token


db = connectors.mongodb_client['stress_lifelog']


router = APIRouter(
    prefix="/annotation/users",
    tags=["/annotation/users"],
    responses = { 404: {"description": "Not Found"}},
)


@router.post("/insert_user", status_code = status.HTTP_201_CREATED, response_model = UserModel)
async def insert_user(request: RequestModifyListDates, user_id: str = Depends(verify_token)):

    """
    Insert a new user into the database.
    NOTE: Refer to the UserModel in the folder schemas for the required fields.
    """

    request = jsonable_encoder(request)
    request['user_id'] = user_id

    user = UserModel(**request)
    user = jsonable_encoder(user)

    try:
        new_user = await db['users'].insert_one(user)
        created_user = await db['users'].find_one({"_id": new_user.inserted_id})
    except Exception as e: 
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
                detail = "User already exists")
    return created_user


@router.post("/insert_dates_to_user", status_code = status.HTTP_201_CREATED, response_model = UserModel)
async def insert_date_to_user(request : RequestModifyListDates, user_id: str = Depends(verify_token)):

    """
    Append a list of dates to the pre-existsing user's list of dates.
    NOTE: Refer to the UserModel in the folder schemas for the required fields.
    """

    request = jsonable_encoder(request)
    dates = request['dates']
    
    try:
        # Insert a list of dates to the end of the list of dates for the user
        _ = await db['users'].update_many({"_id": user_id, }, {"$addToSet": {"dates": {"$each": dates }}}, upsert = True) 
        user = await db['users'].find_one({"_id": user_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
            detail = "Duplicate dates!!!")
    return user


@router.get("/get_dates_from_user", status_code = status.HTTP_200_OK, response_model=ResponseListDates)
async def get_dates_from_user(user_id: str = Depends(verify_token)):
    """
    Get a list of dates from the user.
    NOTE: user_id is the user's unique identifier in the UserModel.
        Refer to the UserModel in the folder schemas for the required fields.
    """

    try:
        dates = await db['users'].find_one({"_id": user_id})
        if dates is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                detail = "User not found")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "Internal Server Error")
    return dates




