from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_current_user
from backend.core.session import get_db
from backend.features.tasks.schema import (
    TaskCreate,
    TaskListResponse,
    TaskResponse,
    TaskUpdate,
)
from backend.features.tasks.usecases import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)
from backend.models.user import User


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create(
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_task(data, current_user, db)


@router.get("", response_model=TaskListResponse)
async def list_all(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    items, total = await list_tasks(current_user, db, skip, limit)
    return TaskListResponse(items=items, total=total)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_one(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_task(task_id, current_user, db)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update(
    task_id: UUID,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await update_task(task_id, data, current_user, db)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await delete_task(task_id, current_user, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)