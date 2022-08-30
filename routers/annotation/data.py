from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from dependencies import verify_token
from schemas.response_schemas import ResponseListStringValue
from schemas.request_schemas import RequestInsertAnnotationValue, RequestInsertDefaultAnnotationData
from schemas.annotation_data_schemas import UserAnnotationList
from internal.db.annotation_list_crud import (
    get_location_list,
    get_stress_level_list,
    get_activity_list,
    insert_to_location_list,
    insert_to_stress_level_list,
    insert_to_activity_list,
    insert_default_annotation_data as insert_default_annotation_data_to_db,
    get_all_annotation_data,
    get_annotation_list as _get_annotation_list,
)


router = APIRouter(
    prefix="/annotation/data",
    tags=['/annotation/data'],
    responses = { 404: {"description": "Not Found"}},
)


@router.post("/insert_default_annotation_data", status_code = status.HTTP_201_CREATED, response_model = UserAnnotationList)
async def insert_default_annotation_data(request : RequestInsertDefaultAnnotationData, user_id: str = Depends(verify_token)):

    """
    Insert a new default annotation data into the database.
    NOTE: Refer to the UserAnnotationList in the folder schemas for the required fields.
    """

    result = await insert_default_annotation_data_to_db(user_id, request)
    if result == False:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
            detail = "Duplicate dates!!!")
    default_annotation_data = await get_all_annotation_data(user_id)
    return default_annotation_data


@router.get("/get_all_annotation_list", status_code = status.HTTP_200_OK, response_model = UserAnnotationList)
async def get_all_annotation_list(user_id: str = Depends(verify_token)):
    
    """
    Get all annotation data from the database.
    """
    try:
        annotation_data = await get_all_annotation_data(user_id)
        if annotation_data is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                detail = "User not found")
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Internal Server Error")
    return annotation_data


@router.post("/insert_to_annotation_list", status_code = status.HTTP_201_CREATED, response_model = ResponseListStringValue)
async def insert_to_annotation_list(request: RequestInsertAnnotationValue, user_id: str = Depends(verify_token)):
    list_type = request.list_type
    value = request.value
    result = True
    if list_type == 'location':
        result = await insert_to_location_list(user_id, value)
    elif list_type == 'stress_level':
        result = await insert_to_stress_level_list(user_id, value)
    elif list_type == 'activity':
        result = await insert_to_activity_list(user_id, value)
    else:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Invalid list type")
    if result == False:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
            detail = "Duplicate value!!!")
    
    annotation_list = await _get_annotation_list(user_id, list_type)
    return annotation_list


@router.get("/get_annotation_list", status_code = status.HTTP_200_OK, response_model = ResponseListStringValue)
async def get_annotation_list(list_type: str, user_id: str = Depends(verify_token)):
    """
    Get a list of all the locations in the database.
    """
    annotation_list = await _get_annotation_list(user_id, list_type)
    if annotation_list is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
            detail = "User not found")
    return annotation_list

