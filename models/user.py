import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

# Імпорт для лінтера
if TYPE_CHECKING:
    from models.order import Order


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Зміна зберігаємо лише захешований пароль
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Додано  статус активності та рольова модель
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    role: Mapped[str] = mapped_column(
        String(50), default="user", server_default="'user'"
    )  # 'user' або 'admin'

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    # Зв'язок (залишається без змін)
    orders: Mapped[List["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
