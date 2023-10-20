from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResponseSchema(BaseModel):

    user_id: int
    job_id: int
    message: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 124,
                    "job_id": 33,
                    "message": "Мне интересна Ваша вакансия!",
                }
            ]
        }
    }


class ResponseInSchema(BaseModel):

    job_id: int
    message: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "job_id": 33,
                    "message": "Мне интересна Ваша вакансия!",
                }
            ]
        }
    }
