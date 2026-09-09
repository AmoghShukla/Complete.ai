from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_current_user
from backend.core.session import get_db
from backend.features.reminders.schema import ReminderCreate, ReminderListResponse, ReminderResponse
from backend.features.reminders.usecases import create_reminder, delete_reminder, list_reminders
from backend.models.user import User


router = APIRouter(tags=["Reminders"])


@router.post("/tasks/{task_id}/reminders", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
async def create(
    task_id: UUID,
    data: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_reminder(task_id, data, current_user, db)


@router.get("/reminders", response_model=ReminderListResponse)
async def list_all(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    items, total = await list_reminders(current_user, db, skip, limit)
    return ReminderListResponse(items=items, total=total)


@router.delete("/reminders/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    reminder_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await delete_reminder(reminder_id, current_user, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)