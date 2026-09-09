from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_current_user
from backend.core.session import get_db
from backend.features.categories.schema import (
    CategoryCreate, CategoryListResponse, CategoryResponse, CategoryUpdate,
)
from backend.features.categories.usecases import (
    create_category, delete_category, get_category, list_categories, update_category,
)
from backend.models.user import User


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create(data: CategoryCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_category(data, current_user, db)


@router.get("", response_model=CategoryListResponse)
async def list_all(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    items, total = await list_categories(current_user, db, skip, limit)
    return CategoryListResponse(items=items, total=total)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_one(category_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_category(category_id, current_user, db)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update(category_id: UUID, data: CategoryUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_category(category_id, data, current_user, db)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(category_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await delete_category(category_id, current_user, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)