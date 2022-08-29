from typing import List
from datetime import date
from fastapi.encoders import jsonable_encoder
from schemas.db_schemas import (
    MomentListByDate,
    MomentListByDateId
)
import sentry_sdk
import connectors


db = connectors.mongodb_client['stress_lifelog']


async def insert_moments(id: MomentListByDateId, moment_list: List[str]) -> bool:
    """
    Insert new moments in a date into the database
    NOTE: Refer to the MomentListByDate in the folder schemas for the required fields.
    """

    request = {
        'id': id,
        'moment_list': moment_list
    }

    moment_list_by_date = MomentListByDate(**request)
    moment_list_by_date = jsonable_encoder(moment_list_by_date)

    try:
        _ = await db['moments'].insert_one(moment_list_by_date)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False
    return True


async def append_moments(id: MomentListByDateId, moment_list: List[str]) -> bool:

    """
    Append new moments into a date of a user into the database
    NOTE: Refer to the MomentListByDate in the folder schemas for the required fields.
    """
    moment_id = MomentListByDateId(**id)
    moment_id = jsonable_encoder(moment_id)
    _moments = moment_list

    try:
        _ = await db['moments'].update_many({"_id": moment_id}, {"$addToSet": {"moment_list": {"$each": _moments }}}, upsert = True)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False
    return True


async def get_moments_by_date(user_id: str, moment_date: str) -> MomentListByDate:
    
    """
    Get all the moments of a user in a date
    """

    moment_id = MomentListByDateId(user_id = user_id, moment_date = moment_date)
    moment_id = jsonable_encoder(moment_id)
    try:
        _moments = await db['moments'].find_one({"_id": moment_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return None
    return _moments