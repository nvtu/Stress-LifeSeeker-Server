from multiprocessing import allow_connection_pickling
from pydantic import BaseModel, Field
from datetime import date, time
from typing import Union, List
from schemas.db_schemas import (
    PhysiologicalData, 
    MomentDetailId,
    MomentDetail,
    MomentMetadata,
)


class RequestModifyListDates(BaseModel):
    dates: List[date] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "dates": [
                    "2020-01-01",
                    "2020-01-02"
                ]
            }
        }

    
class RequestByMomentDate(BaseModel):
    moment_date: date = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "moment_date": "2020-01-01"
            }
        }


class RequestInsertMomentListByDate(BaseModel):
    id: RequestByMomentDate = Field(...)
    moment_list: List[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": {
                    "moment_date": "2020-01-01",
                },
                "moment_list": [
                    "image1",
                    "image2"
                ]
            }
        }


class RequestMomentDetailById(BaseModel):
    moment_date: date = Field(...)
    moment_time: time = Field(alias = 'local_time')

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "moment_date": "2020-01-01",
                "moment_time": "00:00:00"
            }
        }


class RequestInsertMomentDetail(MomentMetadata):
    id: RequestMomentDetailById = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": {
                    "moment_date": "2020-01-01",
                    "moment_time": "00:00:00"
                },
                "utc_time": "00:00:00",
                "image_path": "image1.jpg",
                "other_image_path": "image2.jpg",
                "location": "home",
                "stress_level": "low",
                "activity": "sedentary",
                "heart_rate": {
                    "min_value": 0.0,
                    "max_value": 0.0,
                    "mean_value": 0.0,
                    "std_value": 0.0
                },
                "bvp": {
                    "min_value": 0.0,
                    "max_value": 0.0,
                    "mean_value": 0.0,
                    "std_value": 0.0
                },
                "eda": {
                    "min_value": 0.0,
                    "max_value": 0.0,
                    "mean_value": 0.0,
                    "std_value": 0.0
                },
                "temp": {
                    "min_value": 0.0,
                    "max_value": 0.0,
                    "mean_value": 0.0,
                    "std_value": 0.0
                }
            }
        }



class RequestUpdateMomentDetail(BaseModel):
    id: RequestMomentDetailById = Field(...)
    data_type: str = Field(...)
    value: Union[PhysiologicalData, str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": {
                    "moment_date": "2020-01-01",
                    "moment_time": "00:00:00",
                },
                "data_type": "location",
                "value": "dcu"
                # "data_type": "heart_rate",
                # "value": {
                #     "min_value": 0.0,
                #     "max_value": 0.0,
                #     "mean_value": 0.0,
                #     "std_value": 0.0
                # }
            }
        }