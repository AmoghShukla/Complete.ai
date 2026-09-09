from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.tags import Tag
from backend.models.task import task_tags
from backend.utilities.exceptions import DatabaseError


class TagRepository:
    @staticmethod
    async def create(tag: Tag, db: AsyncSession) -> Tag:
        try:
            db.add(tag)
            await db.commit()
            await db.refresh(tag)
            return tag
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error creating tag") from exc

    @staticmethod
    async def get_by_id(tag_id: UUID, user_id: UUID, db: AsyncSession) -> Tag | None:
        try:
            result = await db.execute(select(Tag).where(Tag.tag_id == tag_id, Tag.user_id == user_id, Tag.is_deleted == False))
            return result.scalars().first()
        except SQLAlchemyError as exc:
            raise DatabaseError("Error fetching tag") from exc

    @staticmethod
    async def get_by_name(name: str, user_id: UUID, db: AsyncSession) -> Tag | None:
        try:
            result = await db.execute(select(Tag).where(Tag.tag_name == name, Tag.user_id == user_id, Tag.is_deleted == False))
            return result.scalars().first()
        except SQLAlchemyError as exc:
            raise DatabaseError("Error checking tag") from exc

    @staticmethod
    async def list_for_user(user_id: UUID, db: AsyncSession, skip: int, limit: int):
        try:
            filters = Tag.user_id == user_id, Tag.is_deleted == False
            result = await db.execute(select(Tag).where(*filters).order_by(Tag.tag_name).offset(skip).limit(limit))
            total = await db.scalar(select(func.count(Tag.tag_id)).where(*filters))
            return list(result.scalars().all()), total or 0
        except SQLAlchemyError as exc:
            raise DatabaseError("Error listing tags") from exc

    @staticmethod
    async def update(tag: Tag, db: AsyncSession) -> Tag:
        try:
            await db.commit()
            await db.refresh(tag)
            return tag
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error updating tag") from exc

    @staticmethod
    async def soft_delete(tag: Tag, db: AsyncSession) -> None:
        try:
            await db.execute(delete(task_tags).where(task_tags.c.tag_id == tag.tag_id))
            tag.is_deleted = True
            await db.commit()
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error deleting tag") from exc