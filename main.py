import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from routers.auth import router as auth_router

# Імпортуємо роутер продуктів
from routers.products import router as products_router
from settings.db import engine, ping

# Налаштування логування
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Блок автоматичного створення таблиць видалено!
    # Тепер за таблиці відповідає лише Alembic.
    yield
    # При вимкненні сервера чистимо пул з'єднань
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# Підключаємо роутери
app.include_router(products_router)
app.include_router(auth_router)


@app.get("/")
def index_root():
    return {"message": "Hello World!"}


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def db_healthcheck():
    is_alive = await ping()
    if not is_alive:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
    return {"status": "healthy", "database": "connected"}
