from pydantic import BaseModel, Field, ConfigDict, field_validator, validator
from typing import Annotated
import datetime
from typing import Optional


class JobSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    salary_from: float = Field(ge=0)
    salary_to: float = Field(ge=0)
    is_active: bool
    created_at: datetime.datetime


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: Optional[float] = Field(ge=0, default=None)
    salary_to: Optional[float] = Field(ge=0, default=None)
    is_active: bool

    @field_validator("salary_to")
    @classmethod
    def password_match(cls, v, values, **kwargs):
        if v is not None and values["salary_from"] is not None:
            if v < values["salary_from"]:
                raise ValueError("Неверный диапазон зарплаты!")
        return v


class JobUpdateSchema(BaseModel):
    id: int
    title: str
    description: str
    salary_from: Optional[float] = Field(ge=0, default=None)
    salary_to: Optional[float] = Field(ge=0, default=None)

    @field_validator("salary_to")
    @classmethod
    def password_match(cls, v, values, **kwargs):
        if v is not None and values["salary_from"] is not None:
            if v < values["salary_from"]:
                raise ValueError("Неверный диапазон зарплаты!")
        return v

# TODO Добавить превалидатор
# TODO добавить в свагер описания полей, значения по умолчанию(примеры)
# TODO переписать @validator
# TODO Валидатор на наличие 2ух полей в контракте