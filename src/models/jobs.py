from db_settings import Base
from typing import Optional, List
import sqlalchemy as sa
from sqlalchemy.orm import relationship, mapped_column, Mapped
import datetime


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Идентификатор вакансии")
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'), comment="Идентификатор пользователя")
    title: Mapped[str] = mapped_column(comment='Название вакансии')
    description: Mapped[str] = mapped_column(comment='Описание вакансии')
    salary_from: Mapped[Optional[float]] = mapped_column(comment='Зарплата от')
    salary_to: Mapped[Optional[float]] = mapped_column(comment='Зарплата до')
    is_active: Mapped[bool] = mapped_column(comment='Активна ли вакансия')
    created_at: Mapped[datetime.datetime] = mapped_column(comment="Время создания записи",
                                                          default=datetime.datetime.utcnow)

    user: Mapped[List["User"]] = relationship(back_populates="jobs")
    responses: Mapped[List["Response"]] = relationship(back_populates="job")
