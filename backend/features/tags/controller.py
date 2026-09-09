from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_current_user
from backend.core.session import get_db
from backend.features.tags.schema import TagCreate, TagListResponse, TagResponse, TagUpdate
from backend.features.tags.usecases import create_tag, delete_tag, get_tag, list_tags, update_tag
from backend.models.user import User


router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create(data: TagCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_tag(data, current_user, db)


@router.get("", response_model=TagListResponse)
async def list_all(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    items, total = await list_tags(current_user, db, skip, limit)
    return TagListResponse(items=items, total=total)


@router.get("/{tag_id}", response_model=TagResponse)
async def get_one(tag_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_tag(tag_id, current_user, db)


@router.patch("/{tag_id}", response_model=TagResponse)
async def update(tag_id: UUID, data: TagUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_tag(tag_id, data, current_user, db)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(tag_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await delete_tag(tag_id, current_user, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)