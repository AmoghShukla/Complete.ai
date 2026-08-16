

class UserRepository:

    async def signup(data, db):
        db.add(data)
        await db.flush()
        await db.refresh(data)
        return data
