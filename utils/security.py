from authx import AuthX, AuthXConfig
from passlib.context import CryptContext

config = AuthXConfig()
config.JWT_SECRET_KEY = (
    "super-secret-key-change-in-production"  # У реальних проєктах береться з .env
)
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["headers"]

security = AuthX(config=config)

# Контекст для хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Перевірка відповідності чистого пароля та його хешу"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Генерація безпечного хешу для збереження в БД"""
    return pwd_context.hash(password)
