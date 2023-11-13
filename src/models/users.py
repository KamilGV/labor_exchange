import datetime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db_settings import Base
import sqlalchemy as sa
from typing import List


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Идентификатор задачи")
    email: Mapped[str] = mapped_column(comment="Email адрес", unique=True)
    name: Mapped[str] = mapped_column(comment="Имя пользователя")
    hashed_password: Mapped[str] = mapped_column(comment="Зашифрованный пароль")
    is_company: Mapped[bool] = mapped_column(comment="Флаг компании")
    created_at: Mapped[datetime.datetime] = mapped_column(comment="Время создания записи",
                                                          default=datetime.datetime.utcnow)

    jobs: Mapped[List["Job"]] = relationship(back_populates="user")
    responses: Mapped[List["Response"]] = relationship(back_populates="user")
