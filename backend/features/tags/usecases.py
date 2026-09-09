from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.features.tags.repository import TagRepository
from backend.features.tags.schema import TagCreate, TagUpdate
from backend.models.tags import Tag
from backend.models.user import User
from backend.utilities.exceptions import AlreadyExistsException, NotFoundException


async def create_tag(data: TagCreate, current_user: User, db: AsyncSession) -> Tag:
    if await TagRepository.get_by_name(data.tag_name, current_user.user_id, db):
        raise AlreadyExistsException("Tag")
    return await TagRepository.create(Tag(user_id=current_user.user_id, **data.model_dump()), db)


async def list_tags(current_user: User, db: AsyncSession, skip: int, limit: int):
    return await TagRepository.list_for_user(current_user.user_id, db, skip, limit)


async def get_tag(tag_id: UUID, current_user: User, db: AsyncSession) -> Tag:
    tag = await TagRepository.get_by_id(tag_id, current_user.user_id, db)
    if tag is None:
        raise NotFoundException("Tag")
    return tag


async def update_tag(tag_id: UUID, data: TagUpdate, current_user: User, db: AsyncSession) -> Tag:
    tag = await get_tag(tag_id, current_user, db)
    if data.tag_name != tag.tag_name and await TagRepository.get_by_name(data.tag_name, current_user.user_id, db):
        raise AlreadyExistsException("Tag")
    tag.tag_name = data.tag_name
    return await TagRepository.update(tag, db)


async def delete_tag(tag_id: UUID, current_user: User, db: AsyncSession) -> None:
    await TagRepository.soft_delete(await get_tag(tag_id, current_user, db), db)