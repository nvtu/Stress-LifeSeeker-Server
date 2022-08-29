from fastapi.encoders import jsonable_encoder
from schemas.db_schemas import (
    MomentDetail,
    MomentDetailId,
    MomentMetadata
)
import sentry_sdk
import connectors
from schemas.request_schemas import RequestUpdateMomentDetail


db = connectors.mongodb_client['stress_lifelog']



async def insert_moment_detail(id: MomentDetailId, moment_detail: MomentMetadata) -> bool:

    """
    Insert new moment detail into the database
    NOTE: Refer to the MomentDetail in the folder schemas for the required fields.
    """
    
    request = {
        'id': id,
        **moment_detail.dict()
    }

    moment_detail = MomentDetail(**request)
    moment_detail = jsonable_encoder(moment_detail)

    try:
        _ = await db['moment_detail'].insert_one(moment_detail)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False
    return True


async def update_moment_detail(user_id: str, request: RequestUpdateMomentDetail) -> bool:

    """
    Update all the fields of a moment detail except the moment id
    NOTE: Refer to the MomentDetail in the folder schemas for the required fields.
    """

    request = jsonable_encoder(request)
    request['id']['user_id'] = user_id

    data_type = request['data_type']
    value = request['value']

    moment_id = MomentDetailId(**request['id'])
    moment_id = jsonable_encoder(moment_id)

    try:
        _ = await db['moment_detail'].update_one({"_id": moment_id}, {"$set": {data_type: value}})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False
    return True


async def get_moment_detail(user_id: str, moment_date: str, moment_time: str):

    """
    Get all the fields of a moment detail
    NOTE: Refer to the MomentDetail in the folder schemas for the required fields.
    """

    moment_id = MomentDetailId(user_id = user_id, moment_date = moment_date, local_time = moment_time)
    moment_id = jsonable_encoder(moment_id)

    try:
        _moment_detail = await db['moment_detail'].find_one({"_id": moment_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return None
    return _moment_detail