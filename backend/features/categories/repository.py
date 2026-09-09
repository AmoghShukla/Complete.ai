from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.category import Category
from backend.utilities.exceptions import DatabaseError


class CategoryRepository:
    @staticmethod
    async def create(category: Category, db: AsyncSession) -> Category:
        try:
            db.add(category)
            await db.commit()
            await db.refresh(category)
            return category
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error creating category") from exc

    @staticmethod
    async def get_by_id(category_id: UUID, user_id: UUID, db: AsyncSession) -> Category | None:
        try:
            result = await db.execute(
                select(Category).where(
                    Category.category_id == category_id,
                    Category.user_id == user_id,
                    Category.is_deleted == False,
                )
            )
            return result.scalars().first()
        except SQLAlchemyError as exc:
            raise DatabaseError("Error fetching category") from exc

    @staticmethod
    async def get_by_name(name: str, user_id: UUID, db: AsyncSession) -> Category | None:
        try:
            result = await db.execute(
                select(Category).where(
                    Category.category_name == name,
                    Category.user_id == user_id,
                    Category.is_deleted == False,
                )
            )
            return result.scalars().first()
        except SQLAlchemyError as exc:
            raise DatabaseError("Error checking category") from exc

    @staticmethod
    async def list_for_user(user_id: UUID, db: AsyncSession, skip: int, limit: int):
        try:
            filters = Category.user_id == user_id, Category.is_deleted == False
            result = await db.execute(
                select(Category)
                .where(*filters)
                .order_by(Category.category_name)
                .offset(skip)
                .limit(limit)
            )
            total = await db.scalar(select(func.count(Category.category_id)).where(*filters))
            return list(result.scalars().all()), total or 0
        except SQLAlchemyError as exc:
            raise DatabaseError("Error listing categories") from exc

    @staticmethod
    async def update(category: Category, db: AsyncSession) -> Category:
        try:
            await db.commit()
            await db.refresh(category)
            return category
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error updating category") from exc

    @staticmethod
    async def soft_delete(category: Category, db: AsyncSession) -> None:
        try:
            category.is_deleted = True
            await db.commit()
        except SQLAlchemyError as exc:
            await db.rollback()
            raise DatabaseError("Error deleting category") from exc