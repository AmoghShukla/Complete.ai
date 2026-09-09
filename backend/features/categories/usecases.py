from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.features.categories.repository import CategoryRepository
from backend.features.categories.schema import CategoryCreate, CategoryUpdate
from backend.models.category import Category
from backend.models.user import User
from backend.utilities.exceptions import AlreadyExistsException, NotFoundException


async def create_category(data: CategoryCreate, current_user: User, db: AsyncSession) -> Category:
    if await CategoryRepository.get_by_name(data.category_name, current_user.user_id, db):
        raise AlreadyExistsException("Category")
    return await CategoryRepository.create(
        Category(user_id=current_user.user_id, **data.model_dump()), db
    )


async def list_categories(current_user: User, db: AsyncSession, skip: int, limit: int):
    return await CategoryRepository.list_for_user(current_user.user_id, db, skip, limit)


async def get_category(category_id: UUID, current_user: User, db: AsyncSession) -> Category:
    category = await CategoryRepository.get_by_id(category_id, current_user.user_id, db)
    if category is None:
        raise NotFoundException("Category")
    return category


async def update_category(
    category_id: UUID, data: CategoryUpdate, current_user: User, db: AsyncSession
) -> Category:
    category = await get_category(category_id, current_user, db)
    changes = data.model_dump(exclude_unset=True)
    if "category_name" in changes and changes["category_name"] != category.category_name:
        if await CategoryRepository.get_by_name(changes["category_name"], current_user.user_id, db):
            raise AlreadyExistsException("Category")
    for field, value in changes.items():
        setattr(category, field, value)
    return await CategoryRepository.update(category, db)


async def delete_category(category_id: UUID, current_user: User, db: AsyncSession) -> None:
    await CategoryRepository.soft_delete(await get_category(category_id, current_user, db), db)