from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.task import Task
from backend.utilities.exceptions import DatabaseError


class TaskRepository:
    @staticmethod
    async def create(task: Task, db: AsyncSession) -> Task:
        try:
            db.add(task)
            await db.commit()
            await db.refresh(task)
            return task
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error creating task") from exc

    @staticmethod
    async def get_by_id(task_id: UUID, user_id: UUID, db: AsyncSession) -> Task | None:
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
            raise DatabaseError("Error fetching task") from exc

    @staticmethod
    async def list_for_user(
        user_id: UUID,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Task], int]:
        try:
            filters = Task.user_id == user_id, Task.is_deleted == False
            result = await db.execute(
                select(Task)
                .where(*filters)
                .order_by(Task.due_date.is_(None), Task.due_date, Task.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            total = await db.scalar(select(func.count(Task.task_id)).where(*filters))
            return list(result.scalars().all()), total or 0
        except SQLAlchemyError as exc:
            raise DatabaseError("Error listing tasks") from exc

    @staticmethod
    async def update(task: Task, db: AsyncSession) -> Task:
        try:
            await db.commit()
            await db.refresh(task)
            return task
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error updating task") from exc

    @staticmethod
    async def soft_delete(task: Task, db: AsyncSession) -> None:
        try:
            task.is_deleted = True
            await db.commit()
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error deleting task") from exc