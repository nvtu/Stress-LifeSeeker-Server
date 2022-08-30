from pydantic import BaseModel
from datetime import date
from typing import List


class ResponseListDates(BaseModel):
    dates: List[date]

    class Config:
        schema_extra = {
            "example": {
                "dates": [
                    "2020-01-01",
                    "2020-01-02",
                    "2020-01-03"
                ]
            }
        }


class ResponseListMoments(BaseModel):
    moment_list: List[str]

    class Config:
        schema_extra = {
            "example": {
                "moment_list": [
                    "20200101_105230",
                    "20200101_105231",
                    "20200101_105232",
                ]
            }
        }


class ResponseListStringValue(BaseModel):
    list_type: str
    data_list: List[str]

    class Config:
        schema_extra = {
            "example": {
                "list_type": "location",
                "data_list": [
                    'Dublin City University',
                    'Home'
                ]
            }
        }