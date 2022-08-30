from pydantic import BaseModel, Field
from typing import List


class UserAnnotationList(BaseModel):
    user_id: str = Field(alias = "_id")
    location_list: List[str] = Field(...)
    stress_level_list: List[str] = Field(...)
    activity_list: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user_id": "nvtu",
                "location_list": ["Home", "Dublin City University"], 
                "stress_level_list": ["Relax", "Low", "Medium", "High"],
                "activity_list": ['Sitting', 'Walking', 'Running', 'Standing', 'Cycling', 'Driving', 'Riding', 'Hiking', 'Swimming', 'Biking']
            }
        }