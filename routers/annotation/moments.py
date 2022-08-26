from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from schemas.db_schemas import (
    MomentListByDate, 
    MomentListByDateId, 
    MomentDetail,
    MomentDetailId,
)
from schemas.request_schemas import (
    RequestUpdateMomentDetail,
    RequestInsertMomentListByDate,
    RequestInsertMomentDetail,
)
import sentry_sdk
import connectors
from schemas.response_schemas import ResponseListMoments
from dependencies import verify_token


db = connectors.mongodb_client['stress_lifelog']


router = APIRouter(
    prefix="/annotation/moments",
    tags=["/annotation/moments"],
    responses = { 404: {"description": "Not Found"}},
)


@router.post("/insert_moments", status_code = status.HTTP_201_CREATED, response_model = MomentListByDate)
async def insert_moments(request: RequestInsertMomentListByDate, user_id: str = Depends(verify_token)):
    """
    Insert new moments in a date into the database
    NOTE: Refer to the MomentListByDate in the folder schemas for the required fields.
    """
    request = jsonable_encoder(request)
    request['id']['user_id'] = user_id

    moment_list_by_date = MomentListByDate(**request)
    moment_list_by_date = jsonable_encoder(moment_list_by_date)

    try:
        new_moment_list_by_date = await db['moments'].insert_one(moment_list_by_date)
        created_moment_list_by_date = await db['moments'].find_one({"_id": new_moment_list_by_date.inserted_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Moments already exists")
    return created_moment_list_by_date


@router.post("/append_moments", status_code = status.HTTP_201_CREATED, response_model = MomentListByDate)
async def append_moments(request: RequestInsertMomentListByDate, user_id: str = Depends(verify_token)):

    """
    Append new moments into a date of a user into the database
    NOTE: Refer to the MomentListByDate in the folder schemas for the required fields.
    """

    request = jsonable_encoder(request)
    request['id']['user_id'] = user_id

    moment_id = MomentListByDateId(**request['id'])
    moment_id = jsonable_encoder(moment_id)
    _moments = request['moment_list']

    try:
        _ = await db['moments'].update_many({"_id": moment_id}, {"$addToSet": {"moment_list": {"$each": _moments }}}, upsert = True)
        _moments = await db['moments'].find_one({"_id": moment_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Duplicate moments!!!")
    return _moments
    

@router.get("/get_moments_by_date", status_code = status.HTTP_200_OK, response_model = ResponseListMoments)
async def get_moments_by_date(moment_date: str, user_id: str = Depends(verify_token)):
    
    """
    Get all the moments of a user in a date
    """

    moment_id = MomentListByDateId(user_id = user_id, moment_date = moment_date)
    moment_id = jsonable_encoder(moment_id)
    try:
        _moments = await db['moments'].find_one({"_id": moment_id})
        if _moments is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No moments found")
        return _moments
    except Exception as e:
        sentry_sdk.capture_exception(e)


# ----------------------------------------------------------------------------------------------------------------------
# MOMENT DETAILS 
# ----------------------------------------------------------------------------------------------------------------------
@router.post("/insert_moment_detail", status_code = status.HTTP_201_CREATED, response_model = MomentDetail)
async def insert_moment_detail(request: RequestInsertMomentDetail, user_id : str = Depends(verify_token)):

    """
    Insert new moment detail into the database
    NOTE: Refer to the MomentDetail in the folder schemas for the required fields.
    """

    request = jsonable_encoder(request)
    request['id']['user_id'] = user_id

    moment_detail = MomentDetail(**request)
    moment_detail = jsonable_encoder(moment_detail)

    try:
        new_moment_detail = await db['moment_detail'].insert_one(moment_detail)
        created_moment_detail = await db['moment_detail'].find_one({"_id": new_moment_detail.inserted_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Duplicate moments!!!")
    return created_moment_detail


@router.post("/update_moment_detail", status_code = status.HTTP_201_CREATED, response_model = MomentDetail)
async def update_moment_detail(request: RequestUpdateMomentDetail, user_id : str = Depends(verify_token)):

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
        _moment_detail = await db['moment_detail'].find_one({"_id": moment_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Update moment details failed!!!")
    return _moment_detail


@router.get("/get_moment_detail", status_code = status.HTTP_200_OK, response_model = MomentDetail)
async def get_moment_detail(moment_date: str, moment_time: str, user_id: str = Depends(verify_token)):

    """
    Get all the fields of a moment detail
    NOTE: Refer to the MomentDetail in the folder schemas for the required fields.
    """

    moment_id = MomentDetailId(user_id = user_id, moment_date = moment_date, local_time = moment_time)
    moment_id = jsonable_encoder(moment_id)

    try:
        _moment_detail = await db['moment_detail'].find_one({"_id": moment_id})
        if _moment_detail is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No moment detail found")
        return _moment_detail
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Internal Server Error")
