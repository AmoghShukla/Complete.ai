from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.features.tasks.repository import TaskRepository
from backend.features.tasks.schema import TaskCreate, TaskUpdate
from backend.models.task import Task
from backend.models.user import User
from backend.utilities.exceptions import NotFoundException


async def create_task(data: TaskCreate, current_user: User, db: AsyncSession) -> Task:
    task = Task(user_id=current_user.user_id, **data.model_dump())
    return await TaskRepository.create(task, db)


async def list_tasks(
    current_user: User,
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> tuple[list[Task], int]:
    return await TaskRepository.list_for_user(current_user.user_id, db, skip, limit)


async def get_task(task_id: UUID, current_user: User, db: AsyncSession) -> Task:
    task = await TaskRepository.get_by_id(task_id, current_user.user_id, db)
    if task is None:
        raise NotFoundException("Task")
    return task


async def update_task(
    task_id: UUID,
    data: TaskUpdate,
    current_user: User,
    db: AsyncSession,
) -> Task:
    task = await get_task(task_id, current_user, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    return await TaskRepository.update(task, db)


async def delete_task(task_id: UUID, current_user: User, db: AsyncSession) -> None:
    task = await get_task(task_id, current_user, db)
    await TaskRepository.soft_delete(task, db)