from pydantic import BaseModel


class RequestById(BaseModel):
    id: str


    class Config:
        schema_extra = {
            "example": {
                "id": "object_id"
            }
        }

