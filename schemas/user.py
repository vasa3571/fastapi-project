from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str  # Додали, бо воно є в моделі
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: str

    class Config:
        from_attributes = True
