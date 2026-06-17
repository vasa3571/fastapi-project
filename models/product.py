from typing import TYPE_CHECKING, List  # Додаємо TYPE_CHECKING

from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

# Цей блок виконається ТІЛЬКИ під час аналізу коду лінтером/IDE
if TYPE_CHECKING:
    from models.order_item import OrderItem


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Зв'язок з елементами замовлення (залишається як у вас)
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")
