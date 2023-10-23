from pydantic import BaseModel, Field, ConfigDict, field_validator, validator
from typing import Annotated
import datetime
from typing import Optional
from pydantic_core.core_schema import FieldValidationInfo


class JobSchema(BaseModel):

    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    salary_from: Optional[float] = Field(ge=0)
    salary_to: Optional[float] = Field(ge=0)
    is_active: bool
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 153,
                    "user_id": 15,
                    "title": "Разработчик ПО",
                    "description": "Требуемый опыт работы: не требуется. Полная занятость, полный день",
                    "salary_from": 20000,
                    "salary_to": 40000,
                    "is_active": True,
                    "created_at": "2023-10-20T07:34:46.940Z"
                }
            ]
        }
    }


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: Optional[float] = Field(ge=0, default=None)
    salary_to: Optional[float] = Field(ge=0, default=None)
    is_active: bool

    @field_validator("salary_to")
    @classmethod
    def salary_range(cls, v, info: FieldValidationInfo, **kwargs):
        if v is not None and info.data["salary_from"] is not None:
            if v < info.data["salary_from"]:
                raise ValueError("Неверный диапазон зарплаты!")
        return v

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Разработчик ПО",
                    "description": "Требуемый опыт работы: 4 года. Полная занятость, полный день",
                    "salary_from": 20000,
                    "salary_to": 40000,
                    "is_active": True,
                }
            ]
        }
    }


class JobUpdateSchema(BaseModel):
    id: int
    title: str
    description: str
    salary_from: Optional[float] = Field(ge=0, default=None)
    salary_to: Optional[float] = Field(ge=0, default=None)

    @field_validator("salary_to")
    @classmethod
    def salary_range(cls, v, info: FieldValidationInfo, **kwargs):
        if v is not None and info.data["salary_from"] is not None:
            if v < info.data["salary_from"]:
                raise ValueError("Неверный диапазон зарплаты!")
        return v

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 12,
                    "title": "Разработчик ПО со знанием Python",
                    "description": "Требуемый опыт работы: 4 года.",
                    "salary_from": 20000,
                    "salary_to": 40000,
                },
                {
                    "title": "Разработчик ПО со знанием Python",
                    "description": "Требуемый опыт работы: 4 года.",
                    "salary_to": 40000,
                }
            ]
        }
    }