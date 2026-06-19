from typing import Optional

from pydantic import BaseModel, Field


# Базова схема з полями, які є спільними для всіх дій
class ProductBase(BaseModel):
    name: str = Field(..., max_length=255, description="Назва товару")
    price: float = Field(..., gt=0, description="Ціна товару повинна бути більшою за 0")
    description: Optional[str] = Field(None, description="Опис товару")


# Схема для створенн
class ProductCreate(ProductBase):
    pass

# Схема для оновлення
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None


# Схема для читання (відповідь сервера, містить id)
class ProductRead(ProductBase):
    id: int

    # Дозволяє Pydantic працювати з об'єктами SQLAlchemy (ORM)
    model_config = {"from_attributes": True}
