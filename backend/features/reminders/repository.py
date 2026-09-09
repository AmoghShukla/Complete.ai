from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.reminder import Reminder
from backend.models.task import Task
from backend.utilities.exceptions import DatabaseError


class ReminderRepository:
    @staticmethod
    async def get_task(task_id: UUID, user_id: UUID, db: AsyncSession) -> Task | None:
        try:
            result = await db.execute(
                select(Task).where(
                    Task.task_id == task_id,
                    Task.user_id == user_id,
                    Task.is_deleted == False,
                )
            )
            return result.scalars().first()
        except SQLAlchemyError as exc:
            raise DatabaseError("Error fetching task for reminder") from exc

    @staticmethod
    async def create(reminder: Reminder, db: AsyncSession) -> Reminder:
        try:
            db.add(reminder)
            await db.commit()
            await db.refresh(reminder)
            return reminder
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error creating reminder") from exc

    @staticmethod
    async def get_by_id(reminder_id: UUID, user_id: UUID, db: AsyncSession) -> Reminder | None:
        try:
            result = await db.execute(
                select(Reminder)
                .join(Reminder.task)
                .where(
                    Reminder.reminder_id == reminder_id,
                    Task.user_id == user_id,
                    Task.is_deleted == False,
                )
            )
            return result.scalars().first()
        except SQLAlchemyError as exc:
            raise DatabaseError("Error fetching reminder") from exc

    @staticmethod
    async def list_for_user(user_id: UUID, db: AsyncSession, skip: int, limit: int):
        try:
            filters = Task.user_id == user_id, Task.is_deleted == False
            result = await db.execute(
                select(Reminder)
                .join(Reminder.task)
                .where(*filters)
                .order_by(Reminder.remind_at)
                .offset(skip)
                .limit(limit)
            )
            total = await db.scalar(
                select(func.count(Reminder.reminder_id)).join(Reminder.task).where(*filters)
            )
            return list(result.scalars().all()), total or 0
        except SQLAlchemyError as exc:
            raise DatabaseError("Error listing reminders") from exc

    @staticmethod
    async def delete(reminder: Reminder, db: AsyncSession) -> None:
        try:
            await db.delete(reminder)
            await db.commit()
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error deleting reminder") from exc

    @staticmethod
    async def get_due(db: AsyncSession, now: datetime) -> list[Reminder]:
        try:
            result = await db.execute(
                select(Reminder)
                .join(Reminder.task)
                .where(
                    Reminder.is_sent == False,
                    Reminder.remind_at <= now,
                    Task.is_deleted == False,
                )
                .order_by(Reminder.remind_at)
                .limit(100)
            )
            return list(result.scalars().all())
        except SQLAlchemyError as exc:
            raise DatabaseError("Error fetching due reminders") from exc

    @staticmethod
    async def mark_sent(reminder: Reminder, db: AsyncSession) -> None:
        try:
            reminder.is_sent = True
            reminder.sent_at = datetime.now(timezone.utc)
            await db.commit()
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error marking reminder as sent") from exc