from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.features.reminders.repository import ReminderRepository
from backend.features.reminders.schema import ReminderCreate
from backend.models.reminder import Reminder
from backend.models.user import User
from backend.utilities.exceptions import BadRequestException, NotFoundException


async def create_reminder(
    task_id: UUID, data: ReminderCreate, current_user: User, db: AsyncSession
) -> Reminder:
    if data.remind_at.tzinfo is None:
        raise BadRequestException("remind_at must include a timezone")
    task = await ReminderRepository.get_task(task_id, current_user.user_id, db)
    if task is None:
        raise NotFoundException("Task")
    return await ReminderRepository.create(
        Reminder(task_id=task.task_id, **data.model_dump()), db
    )


async def list_reminders(current_user: User, db: AsyncSession, skip: int, limit: int):
    return await ReminderRepository.list_for_user(current_user.user_id, db, skip, limit)


async def delete_reminder(reminder_id: UUID, current_user: User, db: AsyncSession) -> None:
    reminder = await ReminderRepository.get_by_id(reminder_id, current_user.user_id, db)
    if reminder is None:
        raise NotFoundException("Reminder")
    await ReminderRepository.delete(reminder, db)