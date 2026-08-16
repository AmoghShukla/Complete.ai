from sqlalchemy.exc import SQLAlchemyError

class UserRepository:

    async def signup(data, db):
        try:
            db.add(data)
            await db.flush()
            await db.refresh(data)
            return data
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError()


