# MONGODB SCHEMAS DEFINITION
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


class MomentListByDate(BaseModel):
    """
    The schema definition for the Moment List By Date Model of the system
    """

    id: PyObjectId = Field(default_factory = PyObjectId, alias = '_id')
    image_list: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                "date": "nvtu_2020-01-01",
                "image_list": [
                    "image1.jpg",
                    "image2.jpg"
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


class MomentDetail(BaseModel):
    """
    The schema definition for the Image Detail Model of the system
    """

    # id: PyObjectId = Field(default_factory = PyObjectId, alias = '_id')
    # Metadata Information
    user_id: str = Field(...)
    date_moment: date = Field(...)
    local_time: time = Field(...)
    utc_time: time = Field(...)
    image_path: str = Field(...)
    other_image_path: str = Field(...)
    
    # Location, activity, and stress
    location: str = Field(...)
    stress: str = Field(...)
    activity: str = Field(...)

    # Physiological data
    heart_rate: PhysiologicalData = Field(...)
    bvp: PhysiologicalData = Field(...) # Blood Volume Pulse
    eda: PhysiologicalData = Field(...) # Electrodermal Activity
    temp: PhysiologicalData = Field(...) # Skin Temperature

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                "id": "nvtu_2020-01-01_00:00:00",
                "user_id": "nvtu",
                "date_moment": "2020-01-01",
                "local_time": "00:00:00",
                "utc_time": "00:00:00",
                "image_path": "image1.jpg",
                "other_image_path": "image2.jpg",
                "location": "home",
                "stress": "low",
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


