from db_settings import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List


class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Идентификатор отклика")
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'), comment="Идентификатор пользователя")
    job_id: Mapped[int] = mapped_column(sa.ForeignKey('jobs.id'), comment="Идентификатор вакансии")
    message: Mapped[str] = mapped_column(comment='Сопроводительное письмо')

    user: Mapped[List["User"]] = relationship(back_populates="responses")
    job: Mapped[List["Job"]] = relationship(back_populates="responses")
