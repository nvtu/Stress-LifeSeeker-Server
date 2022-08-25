# MONGODB SCHEMAS DEFINITION
from msilib import schema
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List
from datetime import date, time


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError('%s is not a valid ObjectId' % value)
        return ObjectId(value)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type = 'string')




class UserModel(BaseModel):
    """
    The schema definition for the User Model of the system
    """

    # id: PyObjectId = Field(default_factory = PyObjectId, alias = '_id')
    user_id: str = Field(alias = "_id")
    dates: List[date] = Field(...)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                "user_id": "nvtu",
                "dates": [
                    "2020-01-01",
                    "2020-01-02"
                ]
            }
        }


class MomentListByDateId(BaseModel):
    user_id: str = Field(...)
    moment_date: date = Field(...)


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                "user_id": "nvtu",
                "moment_date": "2020-01-01"
            }
        }


class MomentListByDate(BaseModel):
    """
    The schema definition for the Moment List By Date Model of the system
    """

    id: MomentListByDateId = Field(alias = '_id')
    moment_list: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                "id": {
                    "user_id": "nvtu",
                    "moment_date": "2020-01-01"
                },
                "moment_list": [
                    "image1",
                    "image2"
                ]
            }
        }


class PhysiologicalData(BaseModel):
    min_value: float = Field(...)
    max_value: float = Field(...)
    mean_value: float = Field(...)
    std_value: float = Field(...)

    class Config:
        schema_extra = {
            'example': {
                "min_value": 0.0,
                "max_value": 0.0,
                "mean_value": 0.0,
                "std_value": 0.0
            }
        }


class MomentDetailId(BaseModel):
    user_id: str = Field(...)
    moment_date: date = Field(alias = 'date')
    local_time: time = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                "user_id": "nvtu",
                "moment_date": "2020-01-01",
                "local_time": "10:52:30"
            }
        }


class MomentMetadata(BaseModel):
    utc_time: time = Field(...)
    image_path: str = Field(...)
    other_image_path: str = Field(...)
    
    # Location, activity, and stress
    location: str = Field(...)
    stress_level: str = Field(...)
    activity: str = Field(...)

    # Physiological data
    heart_rate: PhysiologicalData = Field(...)
    bvp: PhysiologicalData = Field(...) # Blood Volume Pulse
    eda: PhysiologicalData = Field(...) # Electrodermal Activity
    temp: PhysiologicalData = Field(...) # Skin Temperature

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
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



class MomentDetail(MomentMetadata):
    """
    The schema definition for the Image Detail Model of the system
    """

    # Metadata Information
    id: MomentDetailId = Field(alias = '_id')

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                "id": {
                    "user_id": "nvtu",
                    "moment_date": "2020-01-01",
                    "local_time": "10:52:30"
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


