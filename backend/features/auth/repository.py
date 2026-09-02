from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.user import User
from backend.utilities.exceptions import DatabaseError

class UserRepository:

    @staticmethod
    async def signup(data, db):
        try:
            db.add(data)
            await db.commit()
            await db.refresh(data)
            return data
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError()

    @staticmethod
    async def get_user_by_email(email_id: str, db: AsyncSession) -> User | None:
        try:
            result = await db.execute(
                        select(User).where(
                                User.user_email == email_id,
                                User.is_deleted == False
                            )
                        )
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise DatabaseError('Error fetching user by email') from e


