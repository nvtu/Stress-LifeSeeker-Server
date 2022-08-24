from pydantic import BaseModel, Field
from datetime import date


class RequestById(BaseModel):
    id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "object_id"
            }
        }


class RequestMomentDetailById(BaseModel):
    user_id: str = Field(...)
    _date: str = Field(alias = 'date')
    image_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "nvtu",
                "date": "2020-01-01",
                "image_id": "20200101_105230"
            }
        }