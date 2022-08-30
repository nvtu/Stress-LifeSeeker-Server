import connectors
import sentry_sdk
from typing import List, Union
from schemas.annotation_data_schemas import UserAnnotationList
from schemas.request_schemas import RequestInsertDefaultAnnotationData


db = connectors.mongodb_client['stress_lifelog']


async def insert_default_annotation_data(user_id: str, request: RequestInsertDefaultAnnotationData):
    """
    Insert default annotation data into the database.
    """
    try:
        _ = await db['annotation_data_list'].update_one({"_id": user_id}, {"$set": request.dict()}, upsert = True)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False
    return True


async def get_all_annotation_data(user_id: str) -> Union[None, UserAnnotationList]:
    """
    Get all the annotation data for a user.
    """
    try: 
        annotation_data = await db['annotation_data_list'].find_one({"_id": user_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return None
    return annotation_data


async def insert_to_location_list(user_id: str, value: str):
    """
    Insert a new location into the database.
    """
    try:
        _ = await db['annotation_data_list'].update_one({"_id": user_id}, {"$addToSet": {"location_list": value} }, upsert = True)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False
    return True


async def insert_to_stress_level_list(user_id: str, value: str):
    """
    Insert a new stress level into the database.
    """
    try:
        _ = await db['annotation_data_list'].update_one({"_id": user_id}, {"$addToSet": {"stress_level_list": value} }, upsert = True)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False
    return True


async def insert_to_activity_list(user_id: str, value: str):
    """
    Insert a new activity into the database.
    """
    try:
        _ = await db['annotation_data_list'].update_one({"_id": user_id}, {"$addToSet": {"activity_list": value} }, upsert = True)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False
    return True


async def get_location_list(user_id: str):
    """
    Get a list of all the locations in the database.
    """
    try: 
        location_list = await db['annotation_data_list'].find_one({"_id": user_id}, {'_id': 0, "location_list": 1})
        location_list = {
            "list_type": 'location',
            "data_list": location_list["location_list"]
        }
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return None
    return location_list


async def get_stress_level_list(user_id: str):
    """
    Get a list of all the stress levels in the database.
    """
    try: 
        stress_level_list = await db['annotation_data_list'].find_one({"_id": user_id}, {'_id': 0, "stress_level_list": 1})
        stress_level_list = {
            "list_type": 'stress_level',
            "data_list": stress_level_list["stress_level_list"]
        }
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return None
    return stress_level_list


async def get_activity_list(user_id: str):
    """
    Get a list of all the activities in the database.
    """
    try: 
        activity_list = await db['annotation_data_list'].find_one({"_id": user_id}, {'_id': 0, "activity_list": 1})
        activity_list = {
            "list_type": 'activity',
            "data_list": activity_list["activity_list"]
        }
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return None
    return activity_list