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