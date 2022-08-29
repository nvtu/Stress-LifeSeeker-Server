from typing import List
from datetime import date
from fastapi.encoders import jsonable_encoder
from schemas.db_schemas import (
    UserModel
)
import sentry_sdk
import connectors


db = connectors.mongodb_client['stress_lifelog']


async def insert_user(user_id: str, dates: List[date]) -> bool:

    """
    Insert a new user into the database.
    NOTE: Refer to the UserModel in the folder schemas for the required fields.
    """

    request = {
        'user_id': user_id,
        'dates': dates
    }

    user = UserModel(**request)
    user = jsonable_encoder(user)

    try:
        _ = await db['users'].insert_one(user)
    except Exception as e: 
        sentry_sdk.capture_exception(e)
        return False
    return True


async def insert_dates_to_user(user_id: str, dates: List[date]) -> bool:

    """
    Append a list of dates to the pre-existsing user's list of dates.
    NOTE: Refer to the UserModel in the folder schemas for the required fields.
    """

    try:
        # Insert a list of dates to the end of the list of dates for the user
        _ = await db['users'].update_many({"_id": user_id, }, {"$addToSet": {"dates": {"$each": dates }}}, upsert = True) 
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False
    return True


async def get_dates_from_user(user_id: str) -> UserModel:
    """
    Get a list of dates from the user.
    NOTE: user_id is the user's unique identifier in the UserModel.
        Refer to the UserModel in the folder schemas for the required fields.
    """

    try:
        dates = await db['users'].find_one({"_id": user_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return None
    return dates