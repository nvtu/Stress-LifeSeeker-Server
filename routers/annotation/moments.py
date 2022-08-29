from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from schemas.db_schemas import (
    MomentListByDate, 
    MomentDetail,
    MomentDetailId,
    MomentMetadata
)
from schemas.request_schemas import (
    RequestUpdateMomentDetail,
    RequestInsertMomentListByDate,
    RequestInsertMomentDetail,
)
import connectors
from schemas.response_schemas import ResponseListMoments
from dependencies import verify_token
from internal.db.moment_annotation_crud import (
    insert_moments as insert_new_moments,
    append_moments as append_new_moments,
    get_moments_by_date as get_moments,
)
from internal.db.moment_detail_annotation_crud import (
    insert_moment_detail as insert_new_moment_detail,
    update_moment_detail as update_new_moment_detail,
    get_moment_detail as _get_moment_detail,
)


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

    result = await insert_new_moments(**request) 
    if result == False:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Moments already exists")
    new_moment = await get_moments(**request['id'])
    return new_moment


@router.post("/append_moments", status_code = status.HTTP_201_CREATED, response_model = MomentListByDate)
async def append_moments(request: RequestInsertMomentListByDate, user_id: str = Depends(verify_token)):

    """
    Append new moments into a date of a user into the database
    NOTE: Refer to the MomentListByDate in the folder schemas for the required fields.
    """

    request = jsonable_encoder(request)
    request['id']['user_id'] = user_id


    result = await append_new_moments(**request)
    if result == False:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Duplicate moments!!!")

    new_moment = await get_moments(**request['id'])
    return new_moment


@router.get("/get_moments_by_date", status_code = status.HTTP_200_OK, response_model = ResponseListMoments)
async def get_moments_by_date(moment_date: str, user_id: str = Depends(verify_token)):
    
    """
    Get all the moments of a user in a date
    """

    _moments = await get_moments(user_id, moment_date)
    if _moments is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No moments found")
    return _moments


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

    id = request['id']
    moment_id = MomentDetailId(**id)
    del request['id']
    moment_detail = MomentMetadata(**request)

    result = await insert_new_moment_detail(moment_id, moment_detail)
    if result == False:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Duplicate moments!!!")

    id['moment_time'] = id['local_time']
    del id['local_time']
    new_moment_detail = await _get_moment_detail(**id)
    return new_moment_detail


@router.post("/update_moment_detail", status_code = status.HTTP_201_CREATED, response_model = MomentDetail)
async def update_moment_detail(request: RequestUpdateMomentDetail, user_id : str = Depends(verify_token)):

    """
    Update all the fields of a moment detail except the moment id
    NOTE: Refer to the MomentDetail in the folder schemas for the required fields.
    """

    result = await update_new_moment_detail(user_id, request)
    if result == False:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Update moment details failed!!!")

    id = jsonable_encoder(request.id)
    id['user_id'] = user_id
    id['moment_time'] = id['local_time']
    del id['local_time']
    
    moment_detail = await _get_moment_detail(**id)
    return moment_detail


@router.get("/get_moment_detail", status_code = status.HTTP_200_OK, response_model = MomentDetail)
async def get_moment_detail(moment_date: str, moment_time: str, user_id: str = Depends(verify_token)):

    """
    Get all the fields of a moment detail
    NOTE: Refer to the MomentDetail in the folder schemas for the required fields.
    """

    moment_detail = await _get_moment_detail(user_id, moment_date, moment_time)
    if moment_detail is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No moment detail found")
    return moment_detail
