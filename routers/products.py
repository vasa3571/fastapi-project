import logging

from authx import RequestToken
from fastapi import APIRouter, Depends, HTTPException, status

from schemas.product import ProductCreate, ProductRead, ProductUpdate
from services.products import ProductService, get_product_service
from utils.security import security

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get(
    path="/",
    response_model=list[ProductRead],
    tags=["Products"],
)
async def get_products(product_service: ProductService = Depends(get_product_service)):
    try:
        return await product_service.get_all()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get products")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get products",
        ) from exc


@router.get(
    path="/{product_id}",
    response_model=ProductRead,
    tags=["Products"],
)
async def get_product(
    product_id: int, product_service: ProductService = Depends(get_product_service)
):
    try:
        product = await product_service.get_by_id(product_id=product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        return product

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get product with id %d", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get product",
        ) from exc


@router.post(
    path="/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
)
async def create_product(
    product_data: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
    token: RequestToken = Depends(
        security.access_token_required
    ),  # Захист: доступно лише з JWT токеном
):
    try:
        # Ендпойнт виконається, лише якщо передано валідний токен
        return await product_service.create(data=product_data)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to create product")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product",
        ) from exc


@router.put(
    path="/{product_id}",
    response_model=ProductRead,
    tags=["Products"],
)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
):
    try:
        product = await product_service.update(
            product_id=product_id, data=product_update
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        return product

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to update product with id %s", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product",
        ) from exc


@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Products"],
)
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    token: RequestToken = Depends(
        security.access_token_required
    ),  # Захист: перевірка токена
):
    try:
        # Перевірка рольової моделі (RBAC) з метаданих токена
        user_role = token.extra.get("role")
        if user_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action. Admin role required.",
            )

        deleted = await product_service.delete(product_id=product_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        return None

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to delete product with id %s", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product",
        ) from exc
