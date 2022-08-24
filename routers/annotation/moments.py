from importlib.metadata import requires
from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.db_schemas import MomentListByDate, MomentListByDateId
from schemas.request_schemas import RequestMomentDetailById
import sentry_sdk
import connectors
from schemas.response_schemas import ResponseListMoments


db = connectors.mongodb_client['stress_lifelog']


router = APIRouter(
    prefix="/moments",
    tags=["moments"],
    responses = { 404: {"description": "Not Found"}},
)


@router.post("/insert_moments", status_code = status.HTTP_201_CREATED, response_model = MomentListByDate)
async def insert_moments(request: MomentListByDate):
    """
    Insert new moments in a date into the database
    NOTE: Refer to the MomentListByDate in the folder schemas for the required fields.
    """
    moment_list_by_date = jsonable_encoder(request)
    try:
        new_moment_list_by_date = await db['moments'].insert_one(moment_list_by_date)
        created_moment_list_by_date = await db['moments'].find_one({"_id": new_moment_list_by_date.inserted_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Moments already exists")
    return created_moment_list_by_date


@router.post("/append_moments", status_code = status.HTTP_201_CREATED, response_model = MomentListByDate)
async def append_moments(request: MomentListByDate):

    """
    Append new moments into a date of a user into the database
    NOTE: Refer to the MomentListByDate in the folder schemas for the required fields.
    """

    request = jsonable_encoder(request)
    moment_id = request['_id']
    _moments = request['moment_list']
    try:
        _ = await db['moments'].update_many({"_id": moment_id}, {"$addToSet": {"moment_list": {"$each": _moments }}}, upsert = True)
        _moments = await db['moments'].find_one({"_id": moment_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Duplicate moments!!!")
    return _moments
    

@router.post("/get_moments_by_date", status_code = status.HTTP_200_OK, response_model = ResponseListMoments)
async def get_moments_by_date(request: MomentListByDateId):
    """
    Get all the moments of a user in a date
    """

    moment_id = jsonable_encoder(request)
    try:
        _moments = await db['moments'].find_one({"_id": moment_id})
    except Exception as e:
        sentry_sdk.capture_exception(e)
    if _moments is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No moments found")
    return _moments